from dataclasses import dataclass, field
from typing import Any, List
from urllib.parse import urlparse

from bs4 import BeautifulSoup as bs
from django.apps import apps
from wagtail.models import Page


@dataclass
class FieldProcessor:
    obj: object

    wordpress_instance: object = field(init=False)
    wagtail_instance: object = field(init=False)

    richtext_fields: list = field(default_factory=list)
    stream_fields: list = field(default_factory=list)

    def __post_init__(self):
        # get fresh instance of the Wordpress model and the Wagtail model
        wordpress_model = apps.get_model("wp_connector", self.obj.__class__.__name__)
        self.wordpress_instance = wordpress_model.objects.get(id=self.obj.id)

        wagtail_model = apps.get_model(self.wordpress_instance.WAGTAIL_PAGE_MODEL)

        try:
            self.wagtail_instance = wagtail_model.objects.get(
                id=self.wordpress_instance.wagtail_page_id
            )
            self.get_internal_fields_type(self.wagtail_instance)
        except Page.DoesNotExist:
            print(f"No Wagtail page found for {self.obj}")

    def get_internal_fields_type(self, instance):
        # cache the richtext fields and stream fields of the model
        for f in instance._meta.get_fields():
            if (
                f.name in self.wordpress_instance.FIELD_MAPPING.values()
                and f.name in self.wordpress_instance.STREAMFIELD_MAPPING.values()
                and f.get_internal_type() == "JSONField"
            ):
                self.stream_fields.append(f.name)
            elif (
                f.name in self.wordpress_instance.FIELD_MAPPING.values()
                and f.name not in self.wordpress_instance.STREAMFIELD_MAPPING.values()
                and f.get_internal_type() == "TextField"
            ):
                self.richtext_fields.append(f.name)

    def process_fields(self):
        def get_soup(field_value):
            return bs(field_value, "html.parser")

        print("processing fields for ", self.obj)
        for richtext_field in self.richtext_fields:
            field_value = self.wagtail_instance.__dict__[richtext_field]
            if not field_value:
                continue
            soup = get_soup(field_value)
            anchors = soup.find_all("a")
            for a in anchors:
                if self.anchor_type(a) == "internal":
                    anchor_path = self.anchor_path(a)
                    richtext_anchor = self.get_richtext_anchor(anchor_path, a.text)
                    soup.find("a", href=a["href"]).replaceWith(richtext_anchor)
                    field_value = str(soup)
            self.wagtail_instance.__dict__[richtext_field] = field_value

        for stream_field in self.stream_fields:
            stream_blocks = self.wagtail_instance.__dict__[stream_field].__dict__
            raw_data = stream_blocks["_raw_data"]
            if not raw_data:
                continue
            for data in raw_data:
                if data["type"] == "paragraph":
                    soup = get_soup(data["value"])
                    anchors = soup.find_all("a")
                    for a in anchors:
                        if self.anchor_type(a) == "internal":
                            anchor_path = self.anchor_path(a)
                            richtext_anchor = self.get_richtext_anchor(
                                anchor_path, a.text
                            )
                            soup.find("a", href=a["href"]).replaceWith(richtext_anchor)
                            data["value"] = str(soup)
            self.wagtail_instance.__dict__[stream_field].__dict__[
                "_raw_data"
            ] = raw_data

        if hasattr(self, "wagtail_instance"):
            revision = self.wagtail_instance.save_revision()
            revision.publish()
        else:
            print(
                f"Wagtail page not created. {self.wordpress_instance.wagtail_page_id}"
            )

    def get_richtext_anchor(self, anchor_path, anchor):
        # Find the wordpress model with the slug value
        # and update the anchor href attribute with the wagtail page
        # if it exists

        wordpress_collection = WordpressModelCollectionUtils(
            models=["WpPost", "WpPage"]
        )
        wordpress_collection.update_collection_attrs(["id", "wp_id", "wagtail_page_id"])
        wordpress_collection.create_collection()
        list = wordpress_collection.list
        result = list.get(anchor_path)

        if result and result.get("wagtail_page_id"):
            soup = bs("", "html.parser")
            newlink = soup.new_tag("a")
            newlink["linktype"] = "page"
            newlink["id"] = result["wagtail_page_id"]
            newlink.string = anchor
            return newlink
        else:
            print(f"No wagtail page found for {anchor_path}")
            return anchor

    def anchor_path(self, anchor):
        return urlparse(anchor["href"]).path.strip("/")

    def anchor_type(self, anchor):
        if not anchor.get("href"):
            # ignore empty links
            return
        if anchor.get("href").startswith("http://") or anchor.get("href").startswith(
            "https://"
        ):

            if "." in anchor.get("href"):
                # ignore already absolute links and have a dotted domain
                return "external"

        return "internal"


@dataclass
class WordpressModelCollectionUtils:
    """
    A utility class to handle ad hoc lookup queries on the wordpress model records
    and create a collection of the records for easy lookup

    Args:
        models (Any): A list of models to create a collection of
        models_app (str): The app where the models are located
        collection_key (str): The key to use as the collection key
        collection_attrs (List[str]): The attributes to include in the collection

    Raises:
        ValueError: If no models are provided

    Returns:
        WordpressModelCollectionUtils: An instance of the class

    Methods:
        create_collection: Creates a collection of the models
        get: Get a record by the key
        count: Get the count of the collection
        list: Get the collection as a list
        keys: Get the keys of the collection
        values: Get the values of the collection
        items: Get the items of the collection
    """

    models: Any = field(default_factory=list)
    models_app: str = None
    collection_key: str = None
    collection_attrs: List[str] = field(default_factory=list)

    def __post_init__(self):
        if not self.models_app:
            self.models_app = "wp_connector"
        if not self.collection_key:
            self.collection_key = "slug"
        if not self.collection_attrs:
            self.collection_attrs = ["id", "wp_id"]

        if not self.models:
            raise ValueError("No models provided")

        self.model_list = []
        self.all = {}
        self.populate_models(self.models)

    def populate_models(self, models):
        if isinstance(models, str):
            self.model_list.append(apps.get_model(f"{self.models_app}.{models}"))
        elif isinstance(models, list):
            for model in models:
                self.model_list.append(apps.get_model(f"{self.models_app}.{model}"))
        else:
            raise ValueError(
                "Invalid models provided, provide a string or a list of strings"
            )

    def create_collection(self):
        self.all = {}
        for model in self.model_list:
            for record in model.objects.all():
                # try:
                self.all[getattr(record, self.collection_key)] = {
                    attr: getattr(record, attr) for attr in self.collection_attrs
                }
                # except AttributeError:
                #     print(f"Attribute '{self.collection_key}' not found in {model.__name__}")

    def collection_attrs_presets(self, macro):
        # only really useful if you are working with a single model
        # becuase the collection_attrs will be the same for all models
        # and a attribute error will be raised if the attribute is not found
        if not macro:
            return self.collection_attrs

        if macro == "wppost":
            self.collection_attrs = [
                "id",
                "title",
                "slug",
                "content",
                "excerpt",
                "comment_status",
                "author",
                "categories",
                "tags",
                "wagtail_page_id",
            ]

        if macro == "wppage":
            self.collection_attrs = [
                "id",
                "title",
                "slug",
                "content",
                "excerpt",
                "comment_status",
                "author",
                "parent",
                "wagtail_page_id",
            ]

        if macro == "wagtail_page_id":
            self.collection_attrs.append("wagtail_page_id")

        if macro == "reset":
            self.collection_attrs = ["id", "wp_id"]

    def update_collection_attrs(self, attrs):
        self.collection_attrs = attrs

    def set_collection_key(self, key):
        self.collection_key = key

    def get(self, key):
        return self.all.get(key)

    @property
    def count(self):
        return len(self.all)

    @property
    def list(self):
        return self.all

    @property
    def keys(self):
        return self.all.keys()

    @property
    def values(self):
        return self.all.values()

    @property
    def items(self):
        return self.all.items()
