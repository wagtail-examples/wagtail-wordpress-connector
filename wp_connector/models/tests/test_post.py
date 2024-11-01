from django.test import TestCase

from wp_connector.models.post import WPPost


class TestPost(TestCase):
    """
    Test the concrete WPPost class.

    These tests shoud be useful while developing your own implementation because
    they test the existance of the attributes, fields and methods that are expected
    to be implemented.

    If you change the abstract class, you will likely need to change the concrete
    classes as well.
    """

    def test_attibutes(self):
        # attributes
        self.assertTrue(hasattr(WPPost, "SOURCE_URL"))
        self.assertTrue(hasattr(WPPost, "WAGTAIL_PAGE_MODEL"))
        self.assertTrue(hasattr(WPPost, "WAGTAIL_PAGE_MODEL_PARENT"))
        self.assertTrue(hasattr(WPPost, "FIELD_MAPPING"))
        self.assertTrue(hasattr(WPPost, "STREAMFIELD_MAPPING"))

        # fields
        # inherited from abstract
        self.assertTrue(hasattr(WPPost, "wp_id"))
        self.assertTrue(hasattr(WPPost, "wp_foreign_keys"))
        self.assertTrue(hasattr(WPPost, "wp_many_to_many_keys"))
        self.assertTrue(hasattr(WPPost, "wagtail_model"))
        self.assertTrue(hasattr(WPPost, "wp_cleaned_content"))
        self.assertTrue(hasattr(WPPost, "wp_block_content"))
        self.assertTrue(hasattr(WPPost, "wagtail_page_id"))
        # concrete
        self.assertTrue(hasattr(WPPost, "title"))
        self.assertTrue(hasattr(WPPost, "date"))
        self.assertTrue(hasattr(WPPost, "date_gmt"))
        self.assertTrue(hasattr(WPPost, "guid"))
        self.assertTrue(hasattr(WPPost, "modified"))
        self.assertTrue(hasattr(WPPost, "modified_gmt"))
        self.assertTrue(hasattr(WPPost, "slug"))
        self.assertTrue(hasattr(WPPost, "status"))
        self.assertTrue(hasattr(WPPost, "type"))
        self.assertTrue(hasattr(WPPost, "link"))
        self.assertTrue(hasattr(WPPost, "content"))
        self.assertTrue(hasattr(WPPost, "excerpt"))
        self.assertTrue(hasattr(WPPost, "comment_status"))
        self.assertTrue(hasattr(WPPost, "ping_status"))
        self.assertTrue(hasattr(WPPost, "sticky"))
        self.assertTrue(hasattr(WPPost, "format"))
        self.assertTrue(hasattr(WPPost, "template"))
        self.assertTrue(hasattr(WPPost, "author"))
        self.assertTrue(hasattr(WPPost, "categories"))
        self.assertTrue(hasattr(WPPost, "tags"))

        # methods
        # inherited from abstract
        self.assertTrue(hasattr(WPPost, "get_title"))
        self.assertTrue(hasattr(WPPost, "include_fields_initial_import"))
        self.assertTrue(hasattr(WPPost, "process_fields"))
        self.assertTrue(hasattr(WPPost, "process_foreign_keys"))
        self.assertTrue(hasattr(WPPost, "process_many_to_many_keys"))
        self.assertTrue(hasattr(WPPost, "process_clean_fields"))
        self.assertTrue(hasattr(WPPost, "process_block_fields"))

        # not abstract
        self.assertFalse(WPPost._meta.abstract)

    def test_str(self):
        post = WPPost(title="Test Post")
        self.assertEqual(str(post), "Test Post")

    def test_process_foreign_keys(self):
        # test the method that processes the foreign keys
        self.assertEqual(
            WPPost.process_foreign_keys(),
            [{"author": {"model": "WPAuthor", "field": "wp_id"}}],
        )

    def test_process_many_to_many_keys(self):
        # test the method that processes the many to many keys
        self.assertEqual(
            WPPost.process_many_to_many_keys(),
            [
                {
                    "categories": {"model": "WPCategory", "field": "wp_id"},
                    "tags": {"model": "WPTag", "field": "wp_id"},
                }
            ],
        )

    def test_process_fields(self):
        # test the method that processes the fields
        self.assertEqual(
            WPPost.process_fields(),
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
            WPPost.process_clean_fields(),
            [
                {
                    "content": "wp_cleaned_content",
                }
            ],
        )

    def test_process_block_fields(self):
        # test the method that processes the block fields
        self.assertEqual(
            WPPost.process_block_fields(),
            [
                {
                    "wp_cleaned_content": "wp_block_content",
                }
            ],
        )
