from wagtail import hooks

from .views import (
    WPViewSetGroup,
)


@hooks.register("register_admin_viewset")
def register_wp_viewset_group():
    return WPViewSetGroup()
