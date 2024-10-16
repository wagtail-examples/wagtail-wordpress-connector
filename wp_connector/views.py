from wagtail.admin.viewsets.model import ModelViewSet
from wagtail.admin.viewsets.base import ViewSetGroup

from wp_connector.models import (
    WPAuthor,
    WPCategory,
    WPComment,
    WPMedia,
    WPPage,
    WPPost,
    WPTag,
)


class BaseModelViewSet(ModelViewSet):
    model = None
    form_fields = "__all__"
    search_fields = ["name", "slug"]
    icon = "doc-empty"


class AuthorViewSet(BaseModelViewSet):
    model = WPAuthor
    icon = "user"


class CategoryViewSet(BaseModelViewSet):
    model = WPCategory
    icon = "list-ul"


class CommentViewSet(BaseModelViewSet):
    model = WPComment
    icon = "comment"


class MediaViewSet(BaseModelViewSet):
    model = WPMedia
    icon = "image"


class PageViewSet(BaseModelViewSet):
    model = WPPage
    icon = "doc-empty"


class PostViewSet(BaseModelViewSet):
    model = WPPost
    icon = "doc-full"


class TagViewSet(BaseModelViewSet):
    model = WPTag
    icon = "tag"


class WPViewSetGroup(ViewSetGroup):
    menu_icon = "doc-full"
    menu_label = "Wordpress Data"
    menu_order = 400
    items = (
        AuthorViewSet(),
        CategoryViewSet(),
        CommentViewSet(),
        MediaViewSet(),
        PageViewSet(),
        PostViewSet(),
        TagViewSet(),
    )
