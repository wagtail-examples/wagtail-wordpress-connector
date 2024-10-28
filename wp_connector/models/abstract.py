from django.db import models


class WordpressModel(models.Model):
    """ABSTRACT Base model for the Wordpress models.

    All Wordpress models should inherit from this model.

    Attributes: (need to be defined in the child class)
        SOURCE_URL (str): The source URL for the Wordpress object.
        TARGET_WAGTAIL_PAGE_MODEL (str): The target Wagtail page model.

    """

    SOURCE_URL = None  # e.g. "/wp-json/wp/v2/posts"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.SOURCE_URL:
            raise NotImplementedError(
                self._meta.object_name + "Model must have a SOURCE_URL attribute",
            )

    wp_id = models.IntegerField(unique=True, verbose_name="Wordpress ID")
    wp_foreign_keys = models.JSONField(blank=True, null=True)
    wp_many_to_many_keys = models.JSONField(blank=True, null=True)
    wagtail_model = models.JSONField(blank=True, null=True)
    wp_cleaned_content = models.TextField(blank=True, null=True)
    wp_block_content = models.JSONField(blank=True, null=True)
    wagtail_page_id = models.IntegerField(blank=True, null=True)

    class Meta:
        abstract = True

    @property
    def get_title(self):
        """Get the title for the Wordpress object
        either name or title depending on the model."""
        return self.title if hasattr(self, "title") else self.name

    def exclude_fields_initial_import(self):
        """Fields to exclude in the initial import."""
        exclude_foreign_keys = []
        for field in self.process_foreign_keys():
            for key, _ in field.items():
                exclude_foreign_keys.append(key)

        exclude_many_to_many_keys = []
        for field in self.process_many_to_many_keys():
            for key, _ in field.items():
                exclude_many_to_many_keys.append(key)

        return exclude_foreign_keys + exclude_many_to_many_keys

    def include_fields_initial_import(self):
        """Fields to include in the initial import."""
        import_fields = [
            f.name
            for f in self._meta.get_fields()
            if f.name != "id" and f.name not in self.exclude_fields_initial_import(self)
        ]

        return import_fields

    @staticmethod
    def process_fields():
        """Override this method to process fields."""
        return []

    @staticmethod
    def process_foreign_keys():
        """Override this method to process foreign keys."""
        return []

    @staticmethod
    def process_many_to_many_keys():
        """Override this method to process many to many keys."""
        return []

    @staticmethod
    def process_clean_fields():
        """Override this method to process content by cleaning it."""
        return []

    @staticmethod
    def process_block_fields():
        """Override this method to process content by building blocks."""
        return []

    def get_source_url(self):
        """Get the source URL for the Wordpress object."""
        return self.SOURCE_URL.strip("/")


class ExportableMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.WAGTAIL_PAGE_MODEL:
            raise NotImplementedError(
                self._meta.object_name
                + "Model must have a TARGET_WAGTAIL_PAGE_MODEL attribute",
            )

    WAGTAIL_PAGE_MODEL = None  # e.g. "blog.BlogPage"
    WAGTAIL_PAGE_MODEL_PARENT = None  # e.g. "blog.BlogIndexPage"
    FIELD_MAPPING = {}  # e.g. {"title": "title"} {[object_field]: [wagtail_field]}
    WAGTAIL_REQUIRED_FIELDS = []  # e.g. ["title"] [wagtail_field]


class StreamFieldMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.WAGTAIL_PAGE_MODEL:
            raise NotImplementedError(
                self._meta.object_name
                + "Model must have a TARGET_WAGTAIL_PAGE_MODEL attribute",
            )

    STREAMFIELD_MAPPING = {}  # e.g. {[object_field]: [wagtail_field]}

    def get_streamfield_mapping(self):
        """Get the streamfield mapping for the Wordpress object."""
        return self.STREAMFIELD_MAPPING
