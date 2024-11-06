from django.test import TestCase
from wagtail.models import Page

from blog.models import BlogIndexPage, BlogPage
from home.models import HomePage
from wp_connector.models.post import WPPost
from wp_connector.richtext_field_processor import FieldProcessor


class FieldProcessorTest(TestCase):
    def setUp(self):
        """
        Set up 2 x wordpress records and 2 x wagtail records

        There is a link in each body field to the other record (streamfield)
        There is a link in each intro field to the other record (richtext field)
        """

        # wordpress data
        post_data_1 = {
            "wp_id": 1,
            "title": "Test Post 1",
            "slug": "test-post-1",
            "date": "2021-01-01",
            "date_gmt": "2021-01-01",
            "modified": "2021-01-01",
            "modified_gmt": "2021-01-01",
            # # the following values are overridden below
            "content": "",
            "excerpt": "",
            "wagtail_page_id": None,
        }
        wp_instance_1 = WPPost(**post_data_1)
        wp_instance_1.save()

        post_data_2 = {
            "wp_id": 2,
            "title": "Test Post 2",
            "slug": "test-post-2",
            "date": "2021-01-01",
            "date_gmt": "2021-01-01",
            "modified": "2021-01-01",
            "modified_gmt": "2021-01-01",
            # # the following values are overridden below
            "content": "",
            "excerpt": "",
            "wagtail_page_id": None,
        }
        wp_instance_2 = WPPost(**post_data_2)
        wp_instance_2.save()

        wp_instance_1.content = (
            f'<a href="{wp_instance_2.slug}">{wp_instance_2.title}</a>'
        )
        wp_instance_1.excerpt = (
            f'<a href="{wp_instance_2.slug}">{wp_instance_2.title}</a>'
        )
        wp_instance_1.save()

        wp_instance_2.content = (
            f'<a href="{wp_instance_1.slug}">{wp_instance_1.title}</a>'
        )
        wp_instance_2.excerpt = (
            f'<a href="{wp_instance_1.slug}">{wp_instance_1.title}</a>'
        )
        wp_instance_2.save()

        intro_1 = [{"type": "paragraph", "value": wp_instance_1.excerpt}]
        body_1 = [{"type": "paragraph", "value": wp_instance_1.content}]
        intro_2 = [{"type": "paragraph", "value": wp_instance_2.excerpt}]
        body_2 = [{"type": "paragraph", "value": wp_instance_2.content}]

        wagtail_instance_1 = BlogPage(
            title=wp_instance_1.title,
            slug=wp_instance_1.slug,
            intro=intro_1,
            body=body_1,
            date=wp_instance_1.date,
        )

        wagtail_instance_2 = BlogPage(
            title=wp_instance_2.title,
            slug=wp_instance_2.slug,
            intro=intro_2,
            body=body_2,
            date=wp_instance_2.date,
        )

        blog_index = BlogIndexPage(title="Blog Index", slug="blog")
        home_page = HomePage.objects.all().first()
        home_page.add_child(instance=blog_index)
        blog_index.save_revision().publish()

        blog_index.add_child(instance=wagtail_instance_1)
        wagtail_instance_1.save_revision().publish()
        wp_instance_1.wagtail_page_id = wagtail_instance_1.id
        wp_instance_1.save()
        blog_index.add_child(instance=wagtail_instance_2)
        wagtail_instance_2.save_revision().publish()
        wp_instance_2.wagtail_page_id = wagtail_instance_2.id
        wp_instance_2.save()

        self.wp_instance_1 = wp_instance_1
        self.wp_instance_2 = wp_instance_2
        self.wagtail_instance_1 = wagtail_instance_1
        self.wagtail_instance_2 = wagtail_instance_2

        field_processor_1 = FieldProcessor(self.wp_instance_1)
        field_processor_1.process_fields()
        field_processor_2 = FieldProcessor(self.wp_instance_2)
        field_processor_2.process_fields()

    def test_process_fields_wagtail_instance_1(self):
        # get a fresh copy of the wagtail instance
        wagtail_instance = Page.objects.get(
            id=self.wp_instance_1.wagtail_page_id
        ).specific

        # check the intro field
        intro_content = wagtail_instance.intro
        self.assertIsInstance(intro_content, str)
        self.assertEqual(
            intro_content,
            "[{'type': 'paragraph', 'value': '<a id=\"6\" linktype=\"page\">Test Post 2</a>'}]",
        )

        # check the body field
        body_content = wagtail_instance.body.__dict__["_raw_data"]
        self.assertIsInstance(body_content, list)
        self.assertTrue(body_content[0]["type"], "paragraph")
        self.assertTrue(
            body_content[0]["value"], '<a id="6" linktype="page">Test Post 2</a>'
        )

    def test_process_fields_wagtail_instance_2(self):
        # get a fresh copy of the wagtail instance
        wagtail_instance = Page.objects.get(
            id=self.wp_instance_2.wagtail_page_id
        ).specific

        # check the intro field
        intro_content = wagtail_instance.intro
        self.assertIsInstance(intro_content, str)
        self.assertEqual(
            intro_content,
            "[{'type': 'paragraph', 'value': '<a id=\"5\" linktype=\"page\">Test Post 1</a>'}]",
        )

        # check the body field
        body_content = wagtail_instance.body.__dict__["_raw_data"]
        self.assertIsInstance(body_content, list)
        self.assertTrue(body_content[0]["type"], "paragraph")
        self.assertTrue(
            body_content[0]["value"], '<a id="5" linktype="page">Test Post 1</a>'
        )
