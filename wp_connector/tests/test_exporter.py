from django.test import TestCase

from blog.models import BlogCategory, BlogIndexPage, BlogPage
from home.models import HomePage
from wp_connector.exporter import Exporter
from wp_connector.models.author import WPAuthor
from wp_connector.models.category import WPCategory
from wp_connector.models.post import WPPost
from wp_connector.models.tag import WPTag


class TestExporter(TestCase):
    def setUp(self):
        home_page = HomePage.objects.all().first()
        blog_index = BlogIndexPage(title="Blog Index", slug="blog")
        home_page.add_child(instance=blog_index)
        self.blog_index = blog_index

        self.post_data = {
            "wp_id": 1,
            "title": "Test Post",
            "slug": "test-post",
            "date": "2021-01-01",
            "date_gmt": "2021-01-01",
            "modified": "2021-01-01",
            "modified_gmt": "2021-01-01",
            "content": "<h1>Heading</h1><p>Test content</p>",
            "excerpt": "<p>Test excerpt</p>",
        }

    def test_do_create_wagtail_page(self):
        post = WPPost.objects.create(**self.post_data)

        exporter = Exporter(admin=object(), request=object(), obj=post)
        exporter.do_create_wagtail_page()
        self.assertTrue(post.wagtail_page_id)
        blog_page = BlogPage.objects.get(id=post.wagtail_page_id)
        self.assertEqual(blog_page.title, post.title)

    def test_do_update_wagtail_page(self):
        post = WPPost.objects.create(**self.post_data)

        exporter = Exporter(admin=object(), request=object(), obj=post)
        exporter.do_create_wagtail_page()
        post.title = "New title"
        post.save()

        exporter.do_update_wagtail_page()
        blog_page = BlogPage.objects.get(id=post.wagtail_page_id)
        self.assertEqual(blog_page.title, post.title)

    def test_set_author(self):
        author = WPAuthor(wp_id=1, name="Test Author", slug="test-author")
        author.save()

        post = WPPost.objects.create(**self.post_data)
        post.author = author

        exporter = Exporter(admin=object(), request=object(), obj=post)

        exporter.do_create_wagtail_page()
        self.assertTrue(post.wagtail_page_id)
        blog_page = BlogPage.objects.get(id=post.wagtail_page_id)
        self.assertEqual(blog_page.author.name, author.name)

    def test_set_tags(self):
        tag = WPTag(wp_id=1, name="Test Tag", slug="test-tag")
        tag.save()

        self.assertTrue(WPTag.objects.count, 1)

        post = WPPost.objects.create(**self.post_data)
        post.tags.add(tag)

        exporter = Exporter(admin=object(), request=object(), obj=post)

        exporter.do_create_wagtail_page()
        self.assertTrue(post.wagtail_page_id)
        blog_page = BlogPage.objects.get(id=post.wagtail_page_id)
        self.assertTrue(blog_page.tags.count(), 1)
        self.assertTrue(blog_page.tags.first().name, tag.name)

    def test_set_categories(self):
        category = WPCategory(wp_id=1, name="Test Category", slug="test-category")
        category.save()

        self.assertTrue(WPCategory.objects.count, 1)

        post = WPPost.objects.create(**self.post_data)
        post.categories.add(category)

        exporter = Exporter(admin=object(), request=object(), obj=post)

        exporter.do_create_wagtail_page()
        self.assertTrue(post.wagtail_page_id)
        blog_page = BlogPage.objects.get(id=post.wagtail_page_id)
        self.assertTrue(blog_page.categories.count(), 1)
        blog_category = BlogCategory.objects.get(
            id=blog_page.categories.first().category_id
        )
        self.assertEqual(blog_category.name, category.name)
