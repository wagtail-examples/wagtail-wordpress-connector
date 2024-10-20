from dataclasses import dataclass
from django.apps import apps
from django.utils.text import slugify
import urllib

home_page_model = apps.get_model("home.HomePage")


@dataclass
class Exporter:
    admin: object
    request: object
    obj: object

    wagtail_page_model: object = None
    wagtail_page_model_required_fields: list = None
    required_fields: list = None
    field_mapping: dict = None

    def __post_init__(self):
        self.wagtail_page_model = apps.get_model(
            self.obj.WAGTAIL_PAGE_MODEL.split(".")[0],
            self.obj.WAGTAIL_PAGE_MODEL.split(".")[1],
        )
        self.required_fields = self.obj.WAGTAIL_REQUIRED_FIELDS
        self.field_mapping = self.obj.FIELD_MAPPING

        self.wagtail_page_model_required_fields = [
            field.name
            for field in self.wagtail_page_model._meta.fields
            if field.null is False
            and field.blank is False
            and field.name in self.required_fields
        ]

        self.stream_fields = getattr(
            self.obj,
            "WAGTAIL_PAGE_MODEL_STEAM_FIELDS",
            [],
        )

    def do_create_wagtail_page(self):
        if self.fails_required_fields():
            message = f"Failed to create wordpress object ID:{self.obj.wp_id}"
            message += " because of missing required fields."
            return message

        wp_instance = self.admin.model.objects.get(wp_id=self.obj.wp_id)
        if wp_instance.wagtail_page_id:
            return f"Wagtail page already created. {wp_instance.wagtail_page_id}"

        created_wagtail_page = self.wagtail_page_model()
    
        for wp_field, wagtail_field in self.field_mapping.items():
            setattr(
                created_wagtail_page,
                wagtail_field,
                getattr(
                    self.obj,
                    wp_field,
                ),
            )

        parent_page = apps.get_model("home.HomePage").objects.first()
        parent_page.add_child(instance=created_wagtail_page)
        revision = created_wagtail_page.save_revision()
        revision.publish()

        wp_instance.wagtail_page_id = created_wagtail_page.id
        wp_instance.save()

        return f"Created wagtail page ID:{created_wagtail_page.id}"

    def do_update_wagtail_page(self):
        if self.fails_required_fields():
            message = f"Failed to update wordpress object ID:{self.obj.wp_id}"
            message += " because of missing required fields."
            return message

        wp_instance = self.admin.model.objects.get(wp_id=self.obj.wp_id)
        if not wp_instance.wagtail_page_id:
            return f"Wagtail page not created. {wp_instance.wagtail_page_id}"

        updated_wagtail_page = self.wagtail_page_model.objects.get(
            id=wp_instance.wagtail_page_id,
        )

        for wp_field, wagtail_field in self.field_mapping.items():
            setattr(
                updated_wagtail_page,
                wagtail_field,
                getattr(
                    self.obj,
                    wp_field,
                ),
            )

        revision = updated_wagtail_page.save_revision()
        revision.publish()

        return f"Updated wagtail page ID:{updated_wagtail_page.id}"

    def fails_required_fields(self):
        return any(
            not getattr(self.obj, field)
            for field in self.wagtail_page_model_required_fields
        )
