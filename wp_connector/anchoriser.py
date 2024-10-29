from dataclasses import dataclass, field

from django.apps import apps
from wagtail.models import Page


@dataclass
class Anchoriser:
    obj: object

    richtext_fields: list = field(default_factory=list)
    stream_fields: list = field(default_factory=list)

    wordpress_instance: object = field(init=False)
    wagtail_instance: object = field(init=False)

    def __post_init__(self):
        # get fresh instance of the Wordpress model and the Wagtail model
        wordpress_model = apps.get_model("wp_connector", self.obj.__class__.__name__)
        self.wordpress_instance = wordpress_model.objects.get(id=self.obj.id)

        wagtail_instance = Page.objects.get(id=self.wordpress_instance.wagtail_page_id)
        print(wagtail_instance)
