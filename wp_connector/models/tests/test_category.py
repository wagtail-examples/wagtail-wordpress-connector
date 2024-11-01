from django.test import TestCase

from wp_connector.models.category import WPCategory


class TestCategory(TestCase):
    """
    Test the concrete WPCategory class.

    These tests shoud be useful while developing your own implementation because
    they test the existance of the attributes, fields and methods that are expected
    to be implemented.

    If you change the abstract class, you will likely need to change the concrete
    classes as well.
    """

    def test_attibutes(self):
        # attributes
        self.assertTrue(hasattr(WPCategory, "SOURCE_URL"))

        # fields
        # inherited from abstract
        self.assertTrue(hasattr(WPCategory, "wp_id"))
        self.assertTrue(hasattr(WPCategory, "wp_foreign_keys"))
        self.assertTrue(hasattr(WPCategory, "wp_many_to_many_keys"))
        self.assertTrue(hasattr(WPCategory, "wagtail_model"))
        self.assertTrue(hasattr(WPCategory, "wp_cleaned_content"))
        self.assertTrue(hasattr(WPCategory, "wp_block_content"))
        self.assertTrue(hasattr(WPCategory, "wagtail_page_id"))
        # concrete
        self.assertTrue(hasattr(WPCategory, "name"))
        self.assertTrue(hasattr(WPCategory, "count"))
        self.assertTrue(hasattr(WPCategory, "link"))
        self.assertTrue(hasattr(WPCategory, "slug"))
        self.assertTrue(hasattr(WPCategory, "description"))
        self.assertTrue(hasattr(WPCategory, "taxonomy"))
        self.assertTrue(hasattr(WPCategory, "parent"))

        # methods
        self.assertTrue(hasattr(WPCategory, "get_title"))
        # inherited from abstract
        self.assertTrue(hasattr(WPCategory, "exclude_fields_initial_import"))
        self.assertTrue(hasattr(WPCategory, "include_fields_initial_import"))
        self.assertTrue(hasattr(WPCategory, "process_fields"))
        self.assertTrue(hasattr(WPCategory, "process_foreign_keys"))
        self.assertTrue(hasattr(WPCategory, "process_many_to_many_keys"))
        self.assertTrue(hasattr(WPCategory, "process_clean_fields"))
        self.assertTrue(hasattr(WPCategory, "process_block_fields"))

        # not abstract
        self.assertFalse(WPCategory._meta.abstract)

    def test_str(self):
        category = WPCategory(name="Test Category")
        self.assertEqual(str(category), "Test Category")

    def test_process_foreign_links(self):
        # test the method that processes the foreign keys
        self.assertEqual(
            WPCategory.process_foreign_keys(),
            [
                {
                    "parent": {"model": "self", "field": "wp_id"},
                }
            ],
        )
