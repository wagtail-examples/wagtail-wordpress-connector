from django.test import TestCase

from wp_connector.models.media import WPMedia


class TestWPMedia(TestCase):
    """
    Test the WPMedia class.

    These tests shoud be useful while developing your own implementation because
    they test the existance of the attributes, fields and methods that are expected
    to be implemented.

    If you change the abstract class, you will likely need to change the concrete
    classes as well.
    """

    def test_attrs(self):
        # attributes
        self.assertTrue(hasattr(WPMedia, "SOURCE_URL"))

        # fields
        # inherited
        self.assertTrue(hasattr(WPMedia, "wp_id"))
        self.assertTrue(hasattr(WPMedia, "wp_foreign_keys"))
        self.assertTrue(hasattr(WPMedia, "wp_many_to_many_keys"))
        self.assertTrue(hasattr(WPMedia, "wagtail_model"))
        self.assertTrue(hasattr(WPMedia, "wp_cleaned_content"))
        self.assertTrue(hasattr(WPMedia, "wp_block_content"))
        self.assertTrue(hasattr(WPMedia, "wagtail_page_id"))
        # concrete
        self.assertTrue(hasattr(WPMedia, "title"))
        self.assertTrue(hasattr(WPMedia, "date"))
        self.assertTrue(hasattr(WPMedia, "date_gmt"))
        self.assertTrue(hasattr(WPMedia, "guid"))
        self.assertTrue(hasattr(WPMedia, "modified"))
        self.assertTrue(hasattr(WPMedia, "modified_gmt"))
        self.assertTrue(hasattr(WPMedia, "slug"))
        self.assertTrue(hasattr(WPMedia, "status"))
        self.assertTrue(hasattr(WPMedia, "comment_status"))
        self.assertTrue(hasattr(WPMedia, "ping_status"))
        self.assertTrue(hasattr(WPMedia, "type"))
        self.assertTrue(hasattr(WPMedia, "link"))
        self.assertTrue(hasattr(WPMedia, "template"))
        self.assertTrue(hasattr(WPMedia, "description"))
        self.assertTrue(hasattr(WPMedia, "caption"))
        self.assertTrue(hasattr(WPMedia, "alt_text"))
        self.assertTrue(hasattr(WPMedia, "media_type"))
        self.assertTrue(hasattr(WPMedia, "mime_type"))
        self.assertTrue(hasattr(WPMedia, "source_url"))
        self.assertTrue(hasattr(WPMedia, "author"))
        self.assertTrue(hasattr(WPMedia, "post"))

        # methods
        self.assertTrue(hasattr(WPMedia, "get_title"))
        self.assertTrue(hasattr(WPMedia, "exclude_fields_initial_import"))
        self.assertTrue(hasattr(WPMedia, "include_fields_initial_import"))
        self.assertTrue(hasattr(WPMedia, "process_fields"))
        self.assertTrue(hasattr(WPMedia, "process_foreign_keys"))
        self.assertTrue(hasattr(WPMedia, "process_many_to_many_keys"))
        self.assertTrue(hasattr(WPMedia, "process_clean_fields"))
        self.assertTrue(hasattr(WPMedia, "process_block_fields"))

        # is abstract
        self.assertFalse(WPMedia._meta.abstract)

    def test_str(self):
        media = WPMedia(title="Test Media")
        self.assertEqual(str(media), "Test Media")

    def test_process_fields(self):
        # test the method that processes the fields
        self.assertEqual(
            WPMedia.process_fields(),
            [
                {"description": "description.rendered"},
                {"caption": "caption.rendered"},
                {"title": "title.rendered"},
                {"guid": "guid.rendered"},
            ],
        )

    def test_process_foreign_keys(self):
        # test the method that processes the foreign keys
        self.assertEqual(
            WPMedia.process_foreign_keys(),
            [
                {
                    "author": {"model": "WPAuthor", "field": "wp_id"},
                    "post": {"model": "WPPost", "field": "wp_id"},
                }
            ],
        )
