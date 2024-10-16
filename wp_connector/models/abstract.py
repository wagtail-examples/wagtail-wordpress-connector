from django.db import models


class WordpressModel(models.Model):
    """ABSTRACT Base model for the Wordpress models.

    All Wordpress models should inherit from this model.
    """

    # Format: /wp-json/wp/v2/[model_name]
    # This is passed to the wordpress client and appended to WP_HOST
    # It's required on every wordpress model
    SOURCE_URL = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.SOURCE_URL:
            raise NotImplementedError("WordpressModel must have a SOURCE_URL attribute")

    wp_id = models.IntegerField(unique=True, verbose_name="Wordpress ID")
    wp_foreign_keys = models.JSONField(blank=True, null=True)
    wp_many_to_many_keys = models.JSONField(blank=True, null=True)
    wagtail_model = models.JSONField(blank=True, null=True)
    wp_cleaned_content = models.TextField(blank=True, null=True)
    wp_block_content = models.JSONField(blank=True, null=True)

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

    # @staticmethod
    # def clean_content_html(html_content, clean_tags=None):
    #     """Clean the content.

    #     Args:
    #         content (str): The content to clean.
    #         clean_tags (list): A list of tags to clean.

    #     Returns:
    #         str: The cleaned content.
    #     """
    #     if not clean_tags:
    #         clean_tags = getattr(settings, "WPI_CLEAN_TAGS", ["div"])

    #     if html_content:
    #         soup = bs4(html_content, "html.parser")
    #         # find all clean_tags tag name and remove them while keeping their contents
    #         for div in soup.find_all(clean_tags):
    #             div.unwrap()
    #         html_content = str(soup)

    #     return html_content

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


# clean_html = WordpressModel.clean_content_html  # for convenience
