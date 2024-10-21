from django.db import models
from django.utils.safestring import mark_safe

from .abstract import WordpressModel


class WPAuthor(WordpressModel):
    """Model definition for Author. AKA User."""

    SOURCE_URL = "/wp-json/wp/v2/users"

    name = models.CharField(max_length=255, help_text="Display name")
    url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    link = models.URLField()
    slug = models.SlugField()
    avatar_urls = models.URLField(blank=True, null=True)  # comes from avatar_urls.96

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"

    def __str__(self):
        return self.name

    def get_link_link(self, obj):
        link = obj.link
        link = f'<a href="{link}" target="_blank">Open</a>'
        return mark_safe(link)
