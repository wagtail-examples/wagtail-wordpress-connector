from urllib.parse import urlparse

import jmespath
from bs4 import BeautifulSoup as bs
from django.apps import apps

from wp_connector.client import Client
from wp_connector.messages import ClientExitException, ClientMessage


class Importer:
    def __init__(self, url, model_name):
        self.client = Client(url)
        self.netloc = urlparse(url).netloc
        self.model = apps.get_model("wp_connector", model_name)
        self.one_to_many = []
        self.many_to_many = []
        self.import_fields = self.model.include_fields_initial_import(self.model)
        self.client_exception = ClientExitException()
        self.client_message = ClientMessage()

    def import_data(self):
        """
        Import data from wordpress api for each endpoint.
        The actions taken to import each endpoiint reply heavily on the model
        been imported. Most if not all actions are defined in the model. So hopefully this
        class can be used for all models.

        There are 2 stages that happen here:

        Stage 1:
        1. Get the data from the endpoint
        2. Rename the id field to wp_id
        3. Get the data we need from the json response
        4. Update or create the model with the data
        5. Make all relative links absolute

        Stage 2:
        1. Process the foreign keys
        2. Process the many to many keys
        """

        self.client_message.info_message(f"Importing data for {self.model.__name__}...")

        for endpoint in self.client.paged_endpoints:
            json_response = self.client.get(endpoint)

            for item in json_response:
                # rename the id field to wp_id
                item["wp_id"] = item.pop("id")
                data = {
                    field: item[field] for field in self.import_fields if field in item
                }

                # some data is nested in the json response
                # so use jmespath to get to it and update the value
                if hasattr(self.model, "process_fields"):
                    for field in self.model.process_fields():
                        for key, value in field.items():
                            data.update({key: jmespath.search(value, item)})

                # create or update the model with data we have so far
                obj, created = self.model.objects.update_or_create(
                    wp_id=item["wp_id"], defaults=data
                )

                self.make_absolute_links(obj)

                # foreign keys
                # cache each object for later processing
                self.one_to_many.append(obj)
                obj.wp_foreign_keys = self.get_foreign_key_data(
                    self.model.process_foreign_keys, self.model, item
                )

                # many to many keys
                # cache each object for later processing
                self.many_to_many.append(obj)
                obj.wp_many_to_many_keys = self.get_many_to_many_data(
                    self.model.process_many_to_many_keys, item
                )

        # processing foreign keys here as we have access to all the data now
        self.process_one_to_many(self.one_to_many)
        self.process_many_to_many(self.many_to_many)
        self.process_clean_fields(self.clean_fields)

    @staticmethod
    def get_cleaned_data(process_clean_fields, item):
        cleaned_data = []

        def clean_content(content):
            # currently just removes whitespace incl. newlines
            # from the start and end of the content
            # remove br tags if they are a top level tag using beautifulsoup
            # remove empty paragraphs

            soup = bs(content, "html.parser")
            tags = []
            for tag in soup.find_all("br", recursive=False):
                tag.decompose()

            for tag in soup.find_all("p", recursive=False):
                if not tag.text.strip():
                    tag.decompose()

            for tag in soup.find_all(recursive=True):
                tags.append(str(tag))

            return "".join(tags)

        for field in process_clean_fields():
            for key, value in field.items():
                cleaned_data.append(
                    {
                        key: clean_content(jmespath.search(value, item)),
                    }
                )

        return cleaned_data

    @staticmethod
    def get_many_to_many_data(process_many_to_many_keys, item):
        many_to_many_data = []

        for field in process_many_to_many_keys():
            # each field to process
            for key, value in field.items():
                if item[key]:  # some are empty lists so ignore them
                    """
                    TRANSFORM: [key] = {[value] = {model: "WPCategory", field: "wp_id"}}
                    OUTPUT:    [{"categories": {"model": "WPCategory", "where": "wp_id", "value": 38}}]
                    """

                    # assuming all many to many keys are to other models
                    model = apps.get_model("wp_connector", value["model"])

                    # values = item.data[key]
                    many_to_many_data.append(
                        {
                            key: {
                                "model": model.__name__,
                                "where": value["field"],
                                "value": item[key],
                            },
                        }
                    )

        return many_to_many_data

    @staticmethod
    def get_foreign_key_data(process_foreign_keys, current_model, item):
        foreign_key_data = []

        for field in process_foreign_keys():
            # get each field to process
            for key, value in field.items():
                if item[key]:  # some are just 0 so ignore them
                    """e.g.
                    INPUT:     "parent": {"model": "self", "field": "wp_id"},
                    TRANSFORM: [key] = {[value] = {model: "self", field: "wp_id"}}
                    OUTPUT:    {"parent": {"model": "WPCategory", "where": "wp_id", "value": 38}}
                    """
                    # self = a foreign key to the current model
                    # or it's a foreign key to another model
                    model = (
                        current_model
                        if value["model"] == "self"
                        else apps.get_model("wp_connector", value["model"])
                    )

                    foreign_key_data.append(
                        {
                            key: {
                                "model": model.__name__,
                                "where": value["field"],
                                "value": item[key],
                            },
                        }
                    )

        return foreign_key_data

    def make_absolute_links(self, obj):
        """
        Make all relative links absolute.
        This isn't neccessarily required as long as you now all internal links are absolute.
        I've found that on occassions they are not.

        Args:
            obj (object): The object to process

        Returns:
            None

        """
        if hasattr(obj, "FIELD_MAPPING"):
            for field in obj.FIELD_MAPPING.keys():
                # in testing with the wordpress theme data the content here can be flagged by BeautifulSoup
                # as looking like a url, it can be ignored. This should be the case with other data too.
                # e.g. MarkupResemblesLocatorWarning: "***" looks like a URL.
                soup = bs(getattr(obj, field), "html.parser")
                for link in soup.find_all("a"):
                    if not link.get("href"):
                        # ignore empty links
                        continue
                    if link.get("href").startswith("http://") or link.get(
                        "href"
                    ).startswith("https://"):
                        if self.netloc in link.get("href") or "." in link.get("href"):
                            # ignore already absolute links and have a dotted domain
                            continue

                    href = link.get("href")
                    # replace http://
                    if href.startswith("http://"):
                        href = href.replace("http://", "")
                    # replace https://
                    if href.startswith("https://"):
                        href = href.replace("https://", "")
                    # prepend the netloc
                    link["href"] = f"http://{self.netloc}/{href.strip('/')}"
                    self.client_message.success_message(f"Links made absolute {obj}")

                setattr(obj, field, str(soup))

    def process_one_to_many(self, objects):
        self.client_message.info_message("Processing foreign keys...")
        for obj in objects:
            for relation in obj.wp_foreign_keys:
                for field, value in relation.items():
                    try:
                        model = apps.get_model("wp_connector", value["model"])
                        where = value["where"]
                        value = value["value"]
                        setattr(obj, field, model.objects.get(**{where: value}))
                    except model.DoesNotExist:
                        self.client_message.info_message(
                            f"Could not find {model.__name__} with {where}={value}. {obj} with id={obj.id}"
                        )
                obj.save()

    def process_many_to_many(self, objects):
        self.client_message.info_message("Processing many to many keys...")
        for obj in objects:
            for relation in obj.wp_many_to_many_keys:
                related_objects = []
                for field, value in relation.items():
                    model = apps.get_model("wp_connector", value["model"])
                    filter = f"""{value["where"]}__in"""
                    related_objects = model.objects.filter(**{filter: value["value"]})
                    if len(related_objects) != len(value["value"]):
                        self.client_message.info_message(
                            f"""Some {model.__name__} objects could not be found. {obj} with id={obj.id}\n"""
                        )

                for related_object in related_objects:
                    getattr(obj, field).add(related_object)

    @staticmethod
    def process_clean_fields(cleaned_fields):
        sys.stdout.write("Processing clean fields...\n")
        for obj in cleaned_fields:
            for field in obj.cleaned_data:
                for key, value in field.items():
                    setattr(obj, key, value)
            obj.save()
