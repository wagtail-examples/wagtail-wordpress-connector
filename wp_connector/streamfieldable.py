from dataclasses import dataclass

from django.apps import apps


@dataclass
class StreamFieldable:
    """
    Updates a Wagtail page with StreamFields.

    Only operates on StreamField instances.
    """

    wagtail_page_id: int
    wordpress_model: object

    def __post_init__(self):
        self.wagtail_page = (
            apps.get_model("wagtailcore.Page")
            .objects.filter(
                id=self.wagtail_page_id,
            )
            .first()
        )

        if not self.wagtail_page:
            raise ValueError("Wagtail page not found.")
