from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page

from wp_connector.field_panels import WordpressInfoPanel


class HomePage(Page):
    pass


class StandardPage(Page):
    intro = RichTextField(blank=True)
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        WordpressInfoPanel(content="wp_connector.WPPage"),
        FieldPanel("intro"),
        FieldPanel("body"),
    ]
