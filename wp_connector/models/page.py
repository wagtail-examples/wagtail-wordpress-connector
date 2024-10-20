from django.db import models

from .abstract import WordpressModel, ExportableMixin


class WPPage(WordpressModel, ExportableMixin):
    """Model definition for Page."""

    SOURCE_URL = "/wp-json/wp/v2/pages"
    WAGTAIL_PAGE_MODEL = "home.StandardPage"
    WAGTAIL_PAGE_MODEL_PARENT = "home.HomePage"
    WAGTAIL_REQUIRED_FIELDS = ["title"]
    WAGTAIL_PAGE_MODEL_STEAM_FIELDS = [
        # "body",
    ]
    FIELD_MAPPING = {
        "title": "title",
        "content": "body",
        "excerpt": "intro",
    }

    title = models.CharField(max_length=255)
    date = models.DateTimeField()
    date_gmt = models.DateTimeField()
    guid = models.URLField()
    modified = models.DateTimeField()
    modified_gmt = models.DateTimeField()
    slug = models.SlugField()
    status = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    link = models.URLField()
    content = models.TextField(blank=True, null=True)
    excerpt = models.TextField(blank=True, null=True)
    comment_status = models.CharField(max_length=255)
    ping_status = models.CharField(max_length=255)
    sticky = models.BooleanField(default=False)
    template = models.CharField(max_length=255, null=True, blank=True)
    author = models.ForeignKey(
        "wp_connector.WPAuthor",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    parent = models.ForeignKey(
        "wp_connector.WPPage",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Page"
        verbose_name_plural = "Pages"

    def __str__(self):
        return self.title

    @staticmethod
    def process_foreign_keys():
        """These are excluded from the first import and processed later."""
        return [
            {
                "author": {"model": "WPAuthor", "field": "wp_id"},
                "parent": {"model": "WPPage", "field": "wp_id"},
            }
        ]

    @staticmethod
    def process_fields():
        """The value is from other keys of the incoming data."""
        return [
            {"title": "title.rendered"},
            {"content": "content.rendered"},
            {"excerpt": "excerpt.rendered"},
            {"guid": "guid.rendered"},
        ]

    @staticmethod
    def process_clean_fields():
        """Clean the content."""
        return [
            {
                "content": "wp_cleaned_content",
            }
        ]

    @staticmethod
    def process_block_fields():
        """Process the content into blocks."""
        return [
            {
                "wp_cleaned_content": "wp_block_content",
            }
        ]
