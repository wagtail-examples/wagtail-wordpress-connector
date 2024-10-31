from wagtail.snippets.models import register_snippet

from blog.models import BlogCategory

register_snippet(BlogCategory)
