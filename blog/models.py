from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail.admin.panels import (
    FieldPanel,
    InlinePanel,
    ObjectList,
    TabbedInterface,
    TitleFieldPanel,
)
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page
from wagtail.search import index

from home.blocks import StreamBlocks
from wp_connector.field_panels import WordpressInfoPanel


class BlogCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    panels = [
        TitleFieldPanel("name"),
        FieldPanel("slug"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Author(models.Model):
    name = models.CharField(max_length=255)
    author_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("author_image"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Authors"


class BlogTagIndexPage(Page):

    def get_context(self, request):

        # Filter by tag
        tag = request.GET.get("tag")
        blogpages = BlogPage.objects.filter(tags__name=tag)

        # Update template context
        context = super().get_context(request)
        context["blogpages"] = blogpages
        return context


class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [FieldPanel("intro")]

    def get_context(self, request):
        """
        Update context to include only published blog pages, ordered by reverse-chron
        take into account if the categories param is available to filter the reocrds
        """
        context = super().get_context(request)

        qs = BlogPage.objects.live().public().order_by("-date")
        categoy = request.GET.get("category")
        if categoy:
            qs = qs.filter(categories__category__slug=categoy)

        paginator = Paginator(qs, 10)
        page = request.GET.get("page")
        try:
            blogpages = paginator.page(page)
        except PageNotAnInteger:
            blogpages = paginator.page(1)
        except EmptyPage:
            blogpages = paginator.page(paginator.num_pages)

        context["blogpages"] = blogpages
        context["total_pages"] = paginator.num_pages
        context["categories"] = BlogCategory.objects.all()
        return context


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        "BlogPage", related_name="tagged_items", on_delete=models.CASCADE
    )


class BlogPage(Page):
    date = models.DateField("Post date")
    intro = RichTextField(blank=True)
    body = StreamField(
        StreamBlocks(),
        blank=True,
    )
    author = models.ForeignKey(
        "blog.Author",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    search_fields = Page.search_fields + [
        index.SearchField("intro"),
        index.SearchField("body"),
    ]

    content_panels = Page.content_panels + [
        WordpressInfoPanel(content="wp_connector.WPPost"),
        FieldPanel(
            "intro",
            help_text="Introductory text will be displayed on the blog index page",
        ),
        FieldPanel("body", help_text="Full text of the blog post"),
    ]

    metadata_panel = [
        FieldPanel(
            "date", help_text="Choose a post date you want to display to site visitors"
        ),
        FieldPanel("author", help_text="Choose an author of the blog post"),
    ]

    taxonomies_panels = [
        FieldPanel("tags", help_text="Add tags to filter the blog post"),
        InlinePanel(
            "categories",
            help_text="Add categories to group the blog post",
            label="Categories",
        ),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Content"),
            ObjectList(Page.promote_panels, heading="Promote"),
            ObjectList(Page.settings_panels, heading="Settings", classname="settings"),
            ObjectList(metadata_panel, heading="Blog Metadata"),
            ObjectList(taxonomies_panels, heading="Blog Taxonomies"),
        ]
    )

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["tags"] = self.tags.all()
        context["tags_show"] = BlogTagIndexPage.objects.first()
        context["categories"] = self.categories.all()
        context["categories_show"] = BlogIndexPage.objects.first()
        return context


class BlogPageCategory(models.Model):
    page = ParentalKey("BlogPage", related_name="categories", on_delete=models.CASCADE)
    category = models.ForeignKey(
        "blog.BlogCategory", related_name="blog_pages", on_delete=models.CASCADE
    )

    panels = [
        FieldPanel("category"),
    ]

    def __str__(self):
        return self.category.name

    class Meta:
        verbose_name_plural = "Categories"
