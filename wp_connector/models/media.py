from django.db import models

from .abstract import WordpressModel


class WPMedia(WordpressModel):
    """Model definition for Media."""

    SOURCE_URL = "/wp-json/wp/v2/media"

    title = models.CharField(max_length=255)
    date = models.DateTimeField()
    date_gmt = models.DateTimeField()
    guid = models.URLField()
    modified = models.DateTimeField()
    modified_gmt = models.DateTimeField()
    slug = models.SlugField()
    status = models.CharField(max_length=255)
    comment_status = models.CharField(max_length=255)
    ping_status = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    link = models.URLField()
    template = models.CharField(max_length=255)
    description = models.TextField()
    caption = models.TextField()
    alt_text = models.CharField(max_length=255)
    media_type = models.CharField(max_length=255)
    mime_type = models.CharField(max_length=255)
    source_url = models.URLField()
    author = models.ForeignKey(
        "wp_connector.WPAuthor",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    post = models.ForeignKey(
        "wp_connector.WPPost",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Media"
        verbose_name_plural = "Media"

    def __str__(self):
        return self.title

    @staticmethod
    def process_fields():
        """The value is from other keys of the incoming data."""
        return [
            {"description": "description.rendered"},
            {"caption": "caption.rendered"},
            {"title": "title.rendered"},
            {"guid": "guid.rendered"},
        ]

    @staticmethod
    def process_foreign_keys():
        """These are excluded from the first import and processed later."""
        return [
            {
                "author": {"model": "WPAuthor", "field": "wp_id"},
                "post": {"model": "WPPost", "field": "wp_id"},
            }
        ]
