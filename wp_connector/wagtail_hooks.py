from wagtail import hooks
from wagtail.admin.menu import MenuItem
from django.urls import reverse

@hooks.register('register_admin_menu_item')
def register_calendar_menu_item():
    return MenuItem('Import Admin', '/import-admin/', icon_name='sliders')
