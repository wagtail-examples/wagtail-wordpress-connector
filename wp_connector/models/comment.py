from django.db import models

from .abstract import WordpressModel


class WPComment(WordpressModel):
    """Model definition for Comment."""

    SOURCE_URL = "/wp-json/wp/v2/comments"

    author_name = models.CharField(max_length=255)
    author_url = models.URLField()
    date = models.DateTimeField()
    date_gmt = models.DateTimeField()
    content = models.TextField(blank=True, null=True)
    link = models.URLField()
    status = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(max_length=255)
    author_avatar_urls = models.URLField(blank=True, null=True)
    post = models.ForeignKey(
        "wp_connector.WPPost",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    parent = models.ForeignKey(
        "wp_connector.WPComment",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    # is this needed as they all seem to be zero anyway?
    author = models.ForeignKey(
        "wp_connector.WPAuthor",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        return self.author_name

    @staticmethod
    def process_fields():
        """The value is from other keys of the incoming data."""
        return [
            {"content": "content.rendered"},
        ]

    @staticmethod
    def process_foreign_keys():
        """These are excluded from the first import and processed later."""
        return [
            {
                "post": {"model": "WPPost", "field": "wp_id"},
                "parent": {"model": "WPComment", "field": "wp_id"},
                "author": {"model": "WPAuthor", "field": "wp_id"},
            }
        ]
