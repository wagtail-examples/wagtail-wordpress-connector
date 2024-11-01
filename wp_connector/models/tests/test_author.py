from django.test import TestCase

from wp_connector.models.author import WPAuthor


class TestAuthor(TestCase):
    """
    Test the concrete WPAuthor class.

    These tests shoud be useful while developing your own implementation because
    they test the existance of the attributes, fields and methods that are expected
    to be implemented.

    If you change the abstract class, you will likely need to change the concrete
    classes as well.
    """

    def test_attibutes(self):
        # attributes
        self.assertTrue(hasattr(WPAuthor, "SOURCE_URL"))

        # fields
        # inherited from abstract
        self.assertTrue(hasattr(WPAuthor, "wp_id"))
        self.assertTrue(hasattr(WPAuthor, "wp_foreign_keys"))
        self.assertTrue(hasattr(WPAuthor, "wp_many_to_many_keys"))
        self.assertTrue(hasattr(WPAuthor, "wagtail_model"))
        self.assertTrue(hasattr(WPAuthor, "wp_cleaned_content"))
        self.assertTrue(hasattr(WPAuthor, "wp_block_content"))
        self.assertTrue(hasattr(WPAuthor, "wagtail_page_id"))
        # concrete
        self.assertTrue(hasattr(WPAuthor, "name"))
        self.assertTrue(hasattr(WPAuthor, "url"))
        self.assertTrue(hasattr(WPAuthor, "description"))
        self.assertTrue(hasattr(WPAuthor, "link"))
        self.assertTrue(hasattr(WPAuthor, "slug"))
        self.assertTrue(hasattr(WPAuthor, "avatar_urls"))

        # methods
        self.assertTrue(hasattr(WPAuthor, "get_title"))
        # inherited from abstract
        self.assertTrue(hasattr(WPAuthor, "exclude_fields_initial_import"))
        self.assertTrue(hasattr(WPAuthor, "include_fields_initial_import"))
        self.assertTrue(hasattr(WPAuthor, "process_fields"))
        self.assertTrue(hasattr(WPAuthor, "process_foreign_keys"))
        self.assertTrue(hasattr(WPAuthor, "process_many_to_many_keys"))
        self.assertTrue(hasattr(WPAuthor, "process_clean_fields"))
        self.assertTrue(hasattr(WPAuthor, "process_block_fields"))

        # not abstract
        self.assertFalse(WPAuthor._meta.abstract)

    def test_str(self):
        author = WPAuthor(name="Test Author")
        self.assertEqual(str(author), "Test Author")

    def test_get_link_link(self):
        # test the method that generates the link for the author list view
        author = WPAuthor(link="http://localhost:8888")
        self.assertEqual(
            author.get_link_link(author),
            '<a href="http://localhost:8888" target="_blank">Open</a>',
        )
