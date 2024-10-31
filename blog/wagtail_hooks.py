from wagtail.snippets.models import register_snippet

from blog.models import Author, BlogCategory

register_snippet(Author)
register_snippet(BlogCategory)
