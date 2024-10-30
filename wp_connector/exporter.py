from dataclasses import dataclass

from django.apps import apps
from taggit.models import Tag

from blog.models import Author
from wp_connector.streamfieldable import StreamFieldable

# TODO: Better logging of messages


@dataclass
class Exporter:
    """
    Exporter class to create/update wagtail pages from wordpress objects.

    The overall plan is to create a wagtail page for each wordpress object
    but also keep track of each wagtail page linked to a wordpress object.
    We do this by saving the wagtail page ID to the wordpress object.
    This should then keep the Wagtail page models clean and not directly have
    references to the wordpress objects.

    Args:
        admin (object):
                The admin class
        request (object):
                The request object
        obj (object):
                The wordpress object

    Attributes:
        wagtail_page_model (object):
                The wagtail page model
        wagtail_page_model_required_fields (list):
                The required fields for the wagtail page model
        wagtail_page_model_has_author (bool):
                Does the wagtail page model have an author field
        wagtail_page_model_has_tags (bool):
                Does the wagtail page model have a tags field
        ## there will be other foriegn key fields here

        required_fields (list):
                The required fields for the Wagtail page model
        field_mapping (dict):
                The mapping between the wordpress object fields and the wagtail page model fields
    """

    # Args
    admin: object
    request: object
    obj: object

    # Configurations
    wagtail_page_model: object = None
    wagtail_page_model_has_author: bool = False
    wagtail_page_model_has_tags: bool = False
    field_mapping: dict = None

    # this takes precedence over the field_mapping
    # if the field is in the stream_field_mapping
    # it will also need an entry in the field_mapping
    stream_field_mapping: dict = None

    def __post_init__(self):
        self.wagtail_page_model = apps.get_model(
            self.obj.WAGTAIL_PAGE_MODEL.split(".")[0],
            self.obj.WAGTAIL_PAGE_MODEL.split(".")[1],
        )
        self.wagtail_page_model_parent = self.obj.WAGTAIL_PAGE_MODEL_PARENT

        # Wagtail always requires a title field value and that fields should
        # always be included in the field_mapping for a page type

        if "title" not in self.obj.FIELD_MAPPING:
            self.post_init_messages = {
                "message": "Title field is required in a FIELD_MAPPING on the wordpress model",
                "level": "ERROR",
            }
            return

        if not self.obj.title:
            self.post_init_messages = {
                "message": f"Title field is required in the wordpress model {self.obj.id}",
                "level": "ERROR",
                "skip": True,
            }
            return

        self.field_mapping = self.obj.FIELD_MAPPING
        self.stream_field_mapping = self.obj.get_streamfield_mapping()

        if hasattr(self.obj, "author"):
            self.wagtail_page_model_has_author = True

        if hasattr(self.obj, "tags"):
            self.wagtail_page_model_has_tags = True

    def do_create_wagtail_page(self):
        # The wagtail parent page
        parent_page = apps.get_model(
            self.wagtail_page_model_parent.split(".")[0],
            self.wagtail_page_model_parent.split(".")[1],
        ).objects.first()
        if not parent_page:
            return {"message": "No parent page found.", "level": "ERROR"}

        # The worpress model instance
        wp_instance = self.admin.model.objects.get(wp_id=self.obj.wp_id)
        # Ignore if the wagtail page is already created
        if wp_instance.wagtail_page_id:
            return {
                "message": f"Wagtail page already created. {wp_instance.title}",
                "level": "WARNING",
            }

        # Create the wagtail page
        created_wagtail_page = self.wagtail_page_model()
        # Set all the fields
        for wp_field, wagtail_field in self.field_mapping.items():
            if self.stream_field_mapping and wp_field in self.stream_field_mapping:
                stream_field = self.stream_field_mapping[wp_field]
                streamdata = StreamFieldable(
                    obj=self.obj,  # for error messages
                    content=getattr(
                        self.obj,
                        wp_field,
                    ),
                )
                setattr(
                    created_wagtail_page,
                    stream_field,
                    streamdata.streamdata,
                )
            else:
                setattr(
                    created_wagtail_page,
                    wagtail_field,
                    getattr(
                        self.obj,
                        wp_field,
                    ),
                )

        # Set the AUTHOR if the page model has an author
        # Do this before the page is published
        if self.wagtail_page_model_has_author:
            # some don't have an author
            if obj_author := self.obj.author:
                # is the author already a snippet?
                author_snippet, created = Author.objects.get_or_create(
                    name=obj_author.name,
                )
                created_wagtail_page.author = author_snippet

        # Set the TAGS if the page model has tags
        # Do this before the page is published
        if self.wagtail_page_model_has_tags:
            # some don't have tags
            if obj_tags := self.obj.tags.all():
                for obj_tag in obj_tags:
                    # is the tag already available in the Tag model?
                    if tag := Tag.objects.filter(name=obj_tag.name).first():
                        created_wagtail_page.tags.add(tag)
                    else:
                        tag = Tag.objects.create(name=obj_tag.name)
                        created_wagtail_page.tags.add(tag)

        # Add/Save the page
        parent_page.add_child(instance=created_wagtail_page)
        revision = created_wagtail_page.save_revision()
        revision.publish()

        # Save the wagtail page ID to the wordpress model
        # so it can be matched later if required
        wp_instance.wagtail_page_id = created_wagtail_page.id
        wp_instance.save()

        return {
            "message": f"Created wagtail page ID:{created_wagtail_page.id}",
            "level": "SUCCESS",
        }

    def do_update_wagtail_page(self):
        # The wagtail parent page
        parent_page = apps.get_model(
            self.wagtail_page_model_parent.split(".")[0],
            self.wagtail_page_model_parent.split(".")[1],
        ).objects.first()
        if not parent_page:
            return {"message": "No parent page found.", "level": "ERROR"}

        # The worpress model instance
        wp_instance = self.admin.model.objects.get(wp_id=self.obj.wp_id)
        if not wp_instance.wagtail_page_id:
            return f"Wagtail page not created. {wp_instance.wagtail_page_id}"

        # Update the wagtail page
        updated_wagtail_page = self.wagtail_page_model.objects.get(
            id=wp_instance.wagtail_page_id,
        )
        # Set all the fields
        for wp_field, wagtail_field in self.field_mapping.items():
            if self.stream_field_mapping and wp_field in self.stream_field_mapping:
                stream_field = self.stream_field_mapping[wp_field]
                streamdata = StreamFieldable(
                    obj=self.obj,  # for error messages
                    content=getattr(
                        self.obj,
                        wp_field,
                    ),
                )
                setattr(
                    updated_wagtail_page,
                    stream_field,
                    streamdata.streamdata,
                )
            else:
                setattr(
                    updated_wagtail_page,
                    wagtail_field,
                    getattr(
                        self.obj,
                        wp_field,
                    ),
                )

        # Set the AUTHOR if the page model has an author
        # Do this before the page is published
        if self.wagtail_page_model_has_author:
            # some don't have an author
            if obj_author := self.obj.author:
                # is the author already a snippet?
                author_snippet, created = Author.objects.get_or_create(
                    name=obj_author.name,
                )
                updated_wagtail_page.author = author_snippet

        # Set the TAGS if the page model has tags
        # Do this before the page is published
        if self.wagtail_page_model_has_tags:
            # some don't have tags
            if obj_tags := self.obj.tags.all():
                updated_wagtail_page.tags.clear()
                for obj_tag in obj_tags:
                    # is the tag already available in the Tag model?
                    if tag := Tag.objects.filter(name=obj_tag.name).first():
                        updated_wagtail_page.tags.add(tag)
                    else:
                        tag = Tag.objects.create(name=obj_tag.name)
                        updated_wagtail_page.tags.add(tag)

        # Update/Save the page
        revision = updated_wagtail_page.save_revision()
        revision.publish()

        # Dont' update the wagtail page ID here
        # once they are reated they should not change

        return {
            "message": f"Updated wagtail page ID:{updated_wagtail_page.id}",
            "level": "SUCCESS",
        }
