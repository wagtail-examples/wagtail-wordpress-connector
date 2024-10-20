from django import template

from blog.models import BlogIndexPage

register = template.Library()


@register.simple_tag
def get_blog_index_url():
    return BlogIndexPage.objects.first().url
