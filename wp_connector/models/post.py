from django.db import models

from .abstract import ExportableMixin, WordpressModel


class WPPost(WordpressModel, ExportableMixin):
    """Model definition for Post."""

    SOURCE_URL = "/wp-json/wp/v2/posts"
    WAGTAIL_PAGE_MODEL = "blog.BlogPage"
    WAGTAIL_PAGE_MODEL_PARENT = "blog.BlogIndexPage"
    WAGTAIL_REQUIRED_FIELDS = ["title"]
    WAGTAIL_PAGE_MODEL_STEAM_FIELDS = [
        "body",
    ]
    FIELD_MAPPING = {
        "title": "title",
        "content": "body",
        "excerpt": "intro",
        "date": "date",
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
    format = models.CharField(max_length=255)
    template = models.CharField(max_length=255, null=True, blank=True)
    author = models.ForeignKey(
        "wp_connector.WPAuthor",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    categories = models.ManyToManyField(
        "wp_connector.WPCategory",
        blank=True,
    )
    tags = models.ManyToManyField(
        "wp_connector.WPTag",
        blank=True,
    )

    # Makes the django admin to display these fields as
    # a javascript widget
    django_admin_filter_horizontal = ("categories", "tags")

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return self.title

    @staticmethod
    def process_foreign_keys():
        """These are excluded from the first import and processed later."""
        return [{"author": {"model": "WPAuthor", "field": "wp_id"}}]

    @staticmethod
    def process_many_to_many_keys():
        """These are excluded from the first import and processed later."""
        return [
            {
                "categories": {"model": "WPCategory", "field": "wp_id"},
                "tags": {"model": "WPTag", "field": "wp_id"},
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
