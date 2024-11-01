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
        self.assertTrue(hasattr(WordpressModel, "exclude_fields_initial_import"))
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
        class TestModel(WordpressModel):
            pass

        with self.assertRaises(NotImplementedError) as e:
            TestModel()
            self.assertEqual(
                str(e),
                "TestModelModel must have a SOURCE_URL attribute",
            )

        # testing get_source_url
        class TestModel(WordpressModel):
            SOURCE_URL = "http://localhost:8888/wp-json/wp/v2/anyendpoint"

        test_model = TestModel()
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
        class TestModel(WordpressModel):
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

        self.assertEqual(TestModel.process_fields(), ["field"])
        self.assertEqual(
            TestModel.process_foreign_keys(),
            [{"key": {"model": "Model", "field": "field"}}],
        )
        self.assertEqual(
            TestModel.process_many_to_many_keys(),
            [{"key": {"model": "Model", "field": "field"}}],
        )
        self.assertEqual(TestModel.process_clean_fields(), ["field"])
        self.assertEqual(TestModel.process_block_fields(), ["field"])

    def test_get_title(self):
        # returns title
        class TestModel(WordpressModel):
            SOURCE_URL = "http://localhost:8888/wp-json/wp/v2/anyendpoint"

        test_model = TestModel()
        test_model.title = "Title"
        test_model.name = "Name"
        self.assertEqual(test_model.get_title, "Title")

        # returns name
        test_model = TestModel()
        test_model.name = "Name"
        self.assertEqual(test_model.get_title, "Name")

    def test_include_fields_initial_import(self):
        # returns fields
        class TestModel(WordpressModel):
            SOURCE_URL = "http://localhost:8888/wp-json/wp/v2/anyendpoint"

        test_model = TestModel()
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

    def test_exclude_fields_initial_import(self):
        # returns empty list
        class TestModel(WordpressModel):
            SOURCE_URL = "http://localhost:8888/wp-json/wp/v2/anyendpoint"

        test_model = TestModel()
        self.assertEqual(test_model.exclude_fields_initial_import(), [])

        # returns list
        class TestModel(WordpressModel):
            SOURCE_URL = "http://localhost:8888/wp-json/wp/v2/anyendpoint"

            def process_foreign_keys(self):
                return [{"key": {"model": "Model", "field": "field"}}]

            def process_many_to_many_keys(self):
                return [{"key": {"model": "Model", "field": "field"}}]

        test_model = TestModel()
        self.assertEqual(
            test_model.exclude_fields_initial_import(),
            ["key", "key"],
        )


class TestExportableMixin(TestCase):
    def test_attrs(self):
        # attributes
        self.assertTrue(hasattr(ExportableMixin, "WAGTAIL_PAGE_MODEL"))
        self.assertTrue(hasattr(ExportableMixin, "WAGTAIL_PAGE_MODEL_PARENT"))
        self.assertTrue(hasattr(ExportableMixin, "FIELD_MAPPING"))
        self.assertTrue(hasattr(ExportableMixin, "WAGTAIL_REQUIRED_FIELDS"))

        # raises error
        class TestModel(ExportableMixin):
            pass

        with self.assertRaises(NotImplementedError) as e:
            TestModel()
            self.assertEqual(
                str(e),
                "Concrete Wordpress Model must have a WAGTAIL_PAGE_MODEL attribute",
            )

        # doesn't raise an error
        class TestModel(ExportableMixin):
            WAGTAIL_PAGE_MODEL = "home.StandardPage"

        TestModel()


class TestStreamFieldMixin(TestCase):
    def test_attrs(self):
        # raises error
        class TestModel(StreamFieldMixin):
            pass

        with self.assertRaises(NotImplementedError) as e:
            TestModel()
            self.assertEqual(
                str(e),
                "Concrete StreamField Model must have a STREAMFIELD_MAPPING attribute",
            )

        # doesn't raise an error
        class TestModel(StreamFieldMixin):
            STREAMFIELD_MAPPING = {"content": "body"}

        TestModel()

        # get_streamfield_mapping
        class TestModel(StreamFieldMixin):
            STREAMFIELD_MAPPING = {"content": "body"}

        test_model = TestModel()
        self.assertEqual(test_model.get_streamfield_mapping(), {"content": "body"})
