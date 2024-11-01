from django.test import TestCase

from wp_connector.models.comment import WPComment


class TestComment(TestCase):
    """
    Test the concrete WPComment class.

    These tests shoud be useful while developing your own implementation because
    they test the existance of the attributes, fields and methods that are expected
    to be implemented.

    If you change the abstract class, you will likely need to change the concrete
    classes as well.
    """

    def test_attibutes(self):
        # attributes
        self.assertTrue(hasattr(WPComment, "SOURCE_URL"))

        # fields
        # inherited from abstract
        self.assertTrue(hasattr(WPComment, "wp_id"))
        self.assertTrue(hasattr(WPComment, "wp_foreign_keys"))
        self.assertTrue(hasattr(WPComment, "wp_many_to_many_keys"))
        self.assertTrue(hasattr(WPComment, "wagtail_model"))
        self.assertTrue(hasattr(WPComment, "wp_cleaned_content"))
        self.assertTrue(hasattr(WPComment, "wp_block_content"))
        self.assertTrue(hasattr(WPComment, "wagtail_page_id"))
        # concrete
        self.assertTrue(hasattr(WPComment, "author_name"))
        self.assertTrue(hasattr(WPComment, "author_url"))
        self.assertTrue(hasattr(WPComment, "date"))
        self.assertTrue(hasattr(WPComment, "date_gmt"))
        self.assertTrue(hasattr(WPComment, "content"))
        self.assertTrue(hasattr(WPComment, "link"))
        self.assertTrue(hasattr(WPComment, "status"))
        self.assertTrue(hasattr(WPComment, "type"))
        self.assertTrue(hasattr(WPComment, "author_avatar_urls"))
        self.assertTrue(hasattr(WPComment, "post"))
        self.assertTrue(hasattr(WPComment, "parent"))
        self.assertTrue(hasattr(WPComment, "author"))

        # methods
        self.assertTrue(hasattr(WPComment, "get_title"))
        # inherited from abstract
        self.assertTrue(hasattr(WPComment, "exclude_fields_initial_import"))
        self.assertTrue(hasattr(WPComment, "include_fields_initial_import"))
        self.assertTrue(hasattr(WPComment, "process_fields"))
        self.assertTrue(hasattr(WPComment, "process_foreign_keys"))
        self.assertTrue(hasattr(WPComment, "process_many_to_many_keys"))
        self.assertTrue(hasattr(WPComment, "process_clean_fields"))
        self.assertTrue(hasattr(WPComment, "process_block_fields"))

        # not abstract
        self.assertFalse(WPComment._meta.abstract)

    def test_str(self):
        comment = WPComment(author_name="Test Comment")
        self.assertEqual(str(comment), "Test Comment")

    def test_process_fields(self):
        # test the method that processes the fields
        self.assertEqual(
            WPComment.process_fields(),
            [
                {"content": "content.rendered"},
            ],
        )

    def test_process_foreign_keys(self):
        # test the method that processes the foreign keys
        self.assertEqual(
            WPComment.process_foreign_keys(),
            [
                {
                    "post": {"model": "WPPost", "field": "wp_id"},
                    "parent": {"model": "WPComment", "field": "wp_id"},
                    "author": {"model": "WPAuthor", "field": "wp_id"},
                }
            ],
        )
