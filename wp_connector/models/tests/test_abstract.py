from django.test import TestCase

from wp_connector.models.abstract import (
    ExportableMixin,
    StreamFieldMixin,
    WordpressModel,
)


class TestWordpressModel(TestCase):
    """
    Test the abstract WordpressModel class.

    These tests shoud be useful while developing your own implementation because
    they test the existance of the attributes, fields and methods that are expected
    to be implemented.

    If you change the abstract class, you will likely need to change the concrete
    classes as well.
    """

    def test_attrs(self):
        # attributes
        self.assertTrue(hasattr(WordpressModel, "SOURCE_URL"))

        # fields
        self.assertTrue(hasattr(WordpressModel, "wp_id"))
        self.assertTrue(hasattr(WordpressModel, "wp_foreign_keys"))
        self.assertTrue(hasattr(WordpressModel, "wp_many_to_many_keys"))
        self.assertTrue(hasattr(WordpressModel, "wagtail_model"))
        self.assertTrue(hasattr(WordpressModel, "wp_cleaned_content"))
        self.assertTrue(hasattr(WordpressModel, "wp_block_content"))
        self.assertTrue(hasattr(WordpressModel, "wagtail_page_id"))

        # methods
        self.assertTrue(hasattr(WordpressModel, "get_title"))
        self.assertTrue(hasattr(WordpressModel, "include_fields_initial_import"))
        self.assertTrue(hasattr(WordpressModel, "process_fields"))
        self.assertTrue(hasattr(WordpressModel, "process_foreign_keys"))
        self.assertTrue(hasattr(WordpressModel, "process_many_to_many_keys"))
        self.assertTrue(hasattr(WordpressModel, "process_clean_fields"))
        self.assertTrue(hasattr(WordpressModel, "process_block_fields"))

        # is abstract
        self.assertTrue(WordpressModel._meta.abstract)

    def test_source_url(self):
        # raises error if SOURCE_URL is None
        class A(WordpressModel):
            pass

        with self.assertRaises(NotImplementedError) as e:
            A()
            self.assertEqual(
                str(e),
                "TestModelModel must have a SOURCE_URL attribute",
            )

        # testing get_source_url
        class B(WordpressModel):
            SOURCE_URL = "http://localhost:8888/wp-json/wp/v2/anyendpoint"

        test_model = B()
        self.assertEqual(
            test_model.get_source_url(),
            "http://localhost:8888/wp-json/wp/v2/anyendpoint",
        )

    def test_static_methods(self):
        # returns empty list
        self.assertEqual(WordpressModel.process_fields(), [])
        self.assertEqual(WordpressModel.process_foreign_keys(), [])
        self.assertEqual(WordpressModel.process_many_to_many_keys(), [])
        self.assertEqual(WordpressModel.process_clean_fields(), [])
        self.assertEqual(WordpressModel.process_block_fields(), [])

        # returns list
        class C(WordpressModel):
            SOURCE_URL = "http://localhost:8888/wp-json/wp/v2/posts"

            def process_fields():
                return ["field"]

            def process_foreign_keys():
                return [{"key": {"model": "Model", "field": "field"}}]

            def process_many_to_many_keys():
                return [{"key": {"model": "Model", "field": "field"}}]

            def process_clean_fields():
                return ["field"]

            def process_block_fields():
                return ["field"]

        self.assertEqual(C.process_fields(), ["field"])
        self.assertEqual(
            C.process_foreign_keys(),
            [{"key": {"model": "Model", "field": "field"}}],
        )
        self.assertEqual(
            C.process_many_to_many_keys(),
            [{"key": {"model": "Model", "field": "field"}}],
        )
        self.assertEqual(C.process_clean_fields(), ["field"])
        self.assertEqual(C.process_block_fields(), ["field"])

    def test_get_title(self):
        # returns title
        class D(WordpressModel):
            SOURCE_URL = "http://localhost:8888/wp-json/wp/v2/anyendpoint"

        test_model = D()
        test_model.title = "Title"
        test_model.name = "Name"
        self.assertEqual(test_model.get_title, "Title")

        # returns name
        test_model = D()
        test_model.name = "Name"
        self.assertEqual(test_model.get_title, "Name")

    def test_include_fields_initial_import(self):
        # returns fields
        class E(WordpressModel):
            SOURCE_URL = "http://localhost:8888/wp-json/wp/v2/anyendpoint"

        test_model = E()
        test_model.process_foreign_keys = lambda: [
            {"author": {"model": "WPAuthor", "field": "fake_1_id"}}
        ]
        test_model.process_many_to_many_keys = lambda: [
            {
                "categories": {"model": "WPCategory", "field": "fake_2_id"},
            }
        ]
        self.assertEqual(
            test_model.include_fields_initial_import(),
            [
                "wp_id",
                "wp_foreign_keys",
                "wp_many_to_many_keys",
                "wagtail_model",
                "wp_cleaned_content",
                "wp_block_content",
                "wagtail_page_id",
            ],
        )


class TestExportableMixin(TestCase):
    def test_attrs(self):
        # attributes
        self.assertTrue(hasattr(ExportableMixin, "WAGTAIL_PAGE_MODEL"))
        self.assertTrue(hasattr(ExportableMixin, "WAGTAIL_PAGE_MODEL_PARENT"))
        self.assertTrue(hasattr(ExportableMixin, "FIELD_MAPPING"))
        self.assertTrue(hasattr(ExportableMixin, "WAGTAIL_REQUIRED_FIELDS"))

        # raises error
        class A(ExportableMixin):
            pass

        with self.assertRaises(NotImplementedError) as e:
            A()
            self.assertEqual(
                str(e),
                "Concrete Wordpress Model must have a WAGTAIL_PAGE_MODEL attribute",
            )

    def test_attrs_raises_error(self):
        # doesn't raise an error
        class B(ExportableMixin):
            WAGTAIL_PAGE_MODEL = "home.StandardPage"

        B()


class TestStreamFieldMixin(TestCase):
    def test_attrs(self):
        # raises error
        class A(StreamFieldMixin):
            pass

        with self.assertRaises(NotImplementedError) as e:
            A()
            self.assertEqual(
                str(e),
                "Concrete StreamField Model must have a STREAMFIELD_MAPPING attribute",
            )

    def test_attrs_raises_error(self):
        # doesn't raise an error
        class B(StreamFieldMixin):
            STREAMFIELD_MAPPING = {"content": "body"}

        B()

    def test_attrs_streamfield_mapping(self):

        # get_streamfield_mapping
        class C(StreamFieldMixin):
            STREAMFIELD_MAPPING = {"content": "body"}

        test_model = C()
        self.assertEqual(test_model.get_streamfield_mapping(), {"content": "body"})
