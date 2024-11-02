from django.test import TestCase

from wp_connector.models.tag import WPTag


class TestTag(TestCase):
    """
    Test the concrete WPTag class.

    These tests shoud be useful while developing your own implementation because
    they test the existance of the attributes, fields and methods that are expected
    to be implemented.

    If you change the abstract class, you will likely need to change the concrete
    classes as well.
    """

    def test_attibutes(self):
        # attributes
        self.assertTrue(hasattr(WPTag, "SOURCE_URL"))

        # fields
        # inherited from abstract
        self.assertTrue(hasattr(WPTag, "wp_id"))
        self.assertTrue(hasattr(WPTag, "wp_foreign_keys"))
        self.assertTrue(hasattr(WPTag, "wp_many_to_many_keys"))
        self.assertTrue(hasattr(WPTag, "wagtail_model"))
        self.assertTrue(hasattr(WPTag, "wp_cleaned_content"))
        self.assertTrue(hasattr(WPTag, "wp_block_content"))
        self.assertTrue(hasattr(WPTag, "wagtail_page_id"))

        # concrete
        self.assertTrue(hasattr(WPTag, "name"))
        self.assertTrue(hasattr(WPTag, "count"))
        self.assertTrue(hasattr(WPTag, "link"))
        self.assertTrue(hasattr(WPTag, "slug"))
        self.assertTrue(hasattr(WPTag, "description"))
        self.assertTrue(hasattr(WPTag, "taxonomy"))

        # methods
        # inherited from abstract
        self.assertTrue(hasattr(WPTag, "get_title"))
        self.assertTrue(hasattr(WPTag, "include_fields_initial_import"))
        self.assertTrue(hasattr(WPTag, "process_fields"))
        self.assertTrue(hasattr(WPTag, "process_foreign_keys"))
        self.assertTrue(hasattr(WPTag, "process_many_to_many_keys"))
        self.assertTrue(hasattr(WPTag, "process_clean_fields"))
        self.assertTrue(hasattr(WPTag, "process_block_fields"))

        # not abstract
        self.assertFalse(WPTag._meta.abstract)

    def test_str(self):
        tag = WPTag(name="Test Tag")
        self.assertEqual(str(tag), "Test Tag")
