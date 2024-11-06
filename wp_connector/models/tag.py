from django.db import models

from .abstract import WordpressModel


class WPTag(WordpressModel):
    """Model definition for Tags."""

    SOURCE_URL = "/wp-json/wp/v2/tags"

    name = models.CharField(max_length=255)
    count = models.IntegerField(default=0)
    link = models.URLField()
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    taxonomy = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __str__(self):
        return self.name
