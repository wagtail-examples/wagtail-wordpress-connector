from django import template

from app.blog.models import BlogIndexPage

register = template.Library()


@register.simple_tag
def get_blog_index_url():
    try:
        return BlogIndexPage.objects.first().url
    except AttributeError:
        return None
