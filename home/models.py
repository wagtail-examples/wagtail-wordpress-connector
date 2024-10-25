from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page

from home.blocks import StreamBlocks
from wp_connector.field_panels import WordpressInfoPanel

from .blocks import StreamBlock


class HomePage(Page):
    pass


class StandardPage(Page):
    intro = RichTextField(blank=True)
    body = StreamField(StreamBlocks(), blank=True)

    content_panels = Page.content_panels + [
        WordpressInfoPanel(content="wp_connector.WPPage"),
        FieldPanel("intro"),
        FieldPanel("body"),
    ]
