from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import (
    FieldPanel,
)


class HomePage(Page):
    pass


class StandardPage(Page):
    intro = RichTextField(blank=True)
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("body"),
    ]
