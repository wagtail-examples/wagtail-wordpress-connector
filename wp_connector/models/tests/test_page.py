from django.test import TestCase

from wp_connector.models.page import WPPage


class TestPage(TestCase):
    """
    Test the concrete WPPage class.

    These tests shoud be useful while developing your own implementation because
    they test the existance of the attributes, fields and methods that are expected
    to be implemented.

    If you change the abstract class, you will likely need to change the concrete
    classes as well.
    """

    def test_attibutes(self):
        # attributes
        self.assertTrue(hasattr(WPPage, "SOURCE_URL"))
        self.assertTrue(hasattr(WPPage, "WAGTAIL_PAGE_MODEL"))
        self.assertTrue(hasattr(WPPage, "WAGTAIL_PAGE_MODEL_PARENT"))
        self.assertTrue(hasattr(WPPage, "FIELD_MAPPING"))
        self.assertTrue(hasattr(WPPage, "STREAMFIELD_MAPPING"))

        # fields
        # inherited from abstract
        self.assertTrue(hasattr(WPPage, "wp_id"))
        self.assertTrue(hasattr(WPPage, "wp_foreign_keys"))
        self.assertTrue(hasattr(WPPage, "wp_many_to_many_keys"))
        self.assertTrue(hasattr(WPPage, "wagtail_model"))
        self.assertTrue(hasattr(WPPage, "wp_cleaned_content"))
        self.assertTrue(hasattr(WPPage, "wp_block_content"))
        self.assertTrue(hasattr(WPPage, "wagtail_page_id"))
        # concrete
        self.assertTrue(hasattr(WPPage, "title"))
        self.assertTrue(hasattr(WPPage, "date"))
        self.assertTrue(hasattr(WPPage, "date_gmt"))
        self.assertTrue(hasattr(WPPage, "guid"))
        self.assertTrue(hasattr(WPPage, "modified"))
        self.assertTrue(hasattr(WPPage, "modified_gmt"))
        self.assertTrue(hasattr(WPPage, "slug"))
        self.assertTrue(hasattr(WPPage, "status"))
        self.assertTrue(hasattr(WPPage, "type"))
        self.assertTrue(hasattr(WPPage, "link"))
        self.assertTrue(hasattr(WPPage, "content"))
        self.assertTrue(hasattr(WPPage, "excerpt"))
        self.assertTrue(hasattr(WPPage, "comment_status"))
        self.assertTrue(hasattr(WPPage, "ping_status"))
        self.assertTrue(hasattr(WPPage, "sticky"))
        self.assertTrue(hasattr(WPPage, "template"))
        self.assertTrue(hasattr(WPPage, "author"))
        self.assertTrue(hasattr(WPPage, "parent"))

        # methods
        # inherited from abstract
        self.assertTrue(hasattr(WPPage, "get_title"))
        self.assertTrue(hasattr(WPPage, "include_fields_initial_import"))
        self.assertTrue(hasattr(WPPage, "process_fields"))
        self.assertTrue(hasattr(WPPage, "process_foreign_keys"))
        self.assertTrue(hasattr(WPPage, "process_many_to_many_keys"))
        self.assertTrue(hasattr(WPPage, "process_clean_fields"))
        self.assertTrue(hasattr(WPPage, "process_block_fields"))

        # not abstract
        self.assertFalse(WPPage._meta.abstract)

    def test_str(self):
        page = WPPage(title="Test Page")
        self.assertEqual(str(page), "Test Page")

    def test_process_foreign_keys(self):
        # test the method that processes the foreign keys
        self.assertEqual(
            WPPage.process_foreign_keys(),
            [
                {
                    "author": {"model": "WPAuthor", "field": "wp_id"},
                    "parent": {"model": "WPPage", "field": "wp_id"},
                }
            ],
        )

    def test_process_fields(self):
        # test the method that processes the fields
        self.assertEqual(
            WPPage.process_fields(),
            [
                {"title": "title.rendered"},
                {"content": "content.rendered"},
                {"excerpt": "excerpt.rendered"},
                {"guid": "guid.rendered"},
            ],
        )

    def test_process_clean_fields(self):
        # test the method that processes the clean fields
        self.assertEqual(
            WPPage.process_clean_fields(),
            [
                {
                    "content": "wp_cleaned_content",
                }
            ],
        )

    def test_process_block_fields(self):
        # test the method that processes the block fields
        self.assertEqual(
            WPPage.process_block_fields(),
            [
                {
                    "wp_cleaned_content": "wp_block_content",
                }
            ],
        )
