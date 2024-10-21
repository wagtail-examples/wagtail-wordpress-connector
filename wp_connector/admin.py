from django.conf import settings
from django.contrib import admin
from django.utils.safestring import mark_safe
from wagtail.contrib.redirects.models import Redirect
from wagtail.models import Page

from .exporter import Exporter
from .models import WPAuthor, WPCategory, WPComment, WPMedia, WPPage, WPPost, WPTag


class ImportAdmin(admin.AdminSite):
    """
    Admin site for the imported wordpress data
    """

    site_header = "Wordpress Import Admin"
    site_title = "Wordpress Import Admin"
    index_title = "Wordpress Import Admin Dashboard"
    site_url = "/"


import_admin = ImportAdmin(name="wordpress-import-admin")


class BaseAdmin(admin.ModelAdmin):
    """
    Base admin class for all wordpress models

    This class provides some common functionality for all wordpress models.
    It's main purpose is to keep the admin list_display pages
    clean and easier to read.

    1. column ordering
    2. truncate some overly long fields
    3. remove some fields from the list display
    4. add some links to open the original wordpress content
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if hasattr(self.model, "django_admin_filter_horizontal"):
            self.filter_horizontal = self.model.django_admin_filter_horizontal

        self.truncated_length = (
            settings.WPC_TRUNCATE
            if hasattr(
                settings,
                "WPC_TRUNCATE",
            )
            else 36
        )

        # column ordering
        first_fields = [
            "name",
            "title",
            "author_name",
        ]
        last_fields = [
            "wp_id",
            "wp_foreign_keys",
            "wp_many_to_many_keys",
            "wp_cleaned_content",
            "wagtail_model",
            "wp_block_content",
            "id",
            "wagtail_page_id",
        ]

        # these fields will have content truncated
        truncated_fields = [
            "title",
            "name",
            "content",
            "excerpt",
            "description",
            "caption",
        ]

        # these fields will be removed from the list_display
        remove_fields = [
            "wp_foreign_keys",
            "wp_many_to_many_keys",
            "wp_cleaned_content",
            "wp_block_content",
            "wagtail_model",
            "author_avatar_urls",
            "avatar_urls",
            "date",
            "date_gmt",
            "modified",
            "modified_gmt",
        ]

        # these fields will be renamed
        # this is useful when the field name is not very descriptive
        # or when the field name is too long
        # specically used to rename the id field of the wordpress models
        rename_columns = ["id", "import_id"]

        # these fields will be displayed as a link to the
        # original wordpress content
        link_fields = [
            "guid",
            "link",
            "source_url",
        ]

        filter_fields = [
            "parent",
            "status",
            "type",
            "comment_status",
            "count",
        ]

        self.search_fields = [  # these fields will be searchable
            field.name
            for field in self.model._meta.fields
            if field.name in first_fields
        ]

        self.list_filter = [  # these fields will be filterable
            field.name
            for field in self.model._meta.fields
            if field.name in filter_fields
        ]

        self.list_display = self.coerce_list_display_fields(
            self.model,
            remove_fields,
            first_fields,
            last_fields,
            truncated_fields,
            link_fields,
            rename_columns,
        )

    def coerce_list_display_fields(
        self,
        obj,
        remove_fields,
        first_fields,
        last_fields,
        truncated_fields,
        link_fields,
        rename_columns,
    ):
        """
        Return the list_display fields for a model

        Args:
            obj (Model): The model to get the fields for.
            remove_fields (list): Fields to remove from the list_display.
            first_fields (list): Fields to display first.
            last_fields (list): Fields to display last.
            truncated_fields (list): Fields to truncate.
            link_fields (list): Fields to display as a link.

        Returns:
            list: The list_display fields.
        """
        # get the fields in the order they are defined in the model
        # and sort them alphabetically
        fields = sorted([field.name for field in obj._meta.fields])

        # move the first and last fields to the front and back
        # this results in a column ordering for the list display
        for field in first_fields:
            if field in fields:
                fields.remove(field)
                fields.insert(0, field)

        for field in last_fields:
            if field in fields:
                fields.remove(field)
                fields.append(field)

        # truncate the content of some fields
        # this results in a cleaner list display by reducing the
        # horizonal space taken up by the columns
        for field in truncated_fields:
            if field in fields:
                position = fields.index(field)
                fields.insert(position, f"get_truncated_{field}")
                fields.remove(field)

        # remove some fields from the list display
        # this results in a cleaner list display by removing
        # fields that are not very usful in the list display
        for field in remove_fields:
            if field in fields:
                fields.remove(field)

        # add some links to the original wordpress content
        # this results in a more interactive list display by
        # providing links to the original wordpress content
        for field in link_fields:
            if field in fields:
                position = fields.index(field)
                fields.insert(position, f"get_link_{field}")
                fields.remove(field)

        # rename some columns
        for field in rename_columns:
            if field in fields:
                position = fields.index(field)
                fields.insert(position, f"get_renamed_{field}")
                fields.remove(field)

        return fields

    def get_renamed_id(self, obj):
        return obj.id

    def get_truncated_content(self, obj):
        # truncate the content field
        return (
            obj.content[: self.truncated_length] + "..."
            if len(obj.content) > self.truncated_length
            else obj.content
        )

    def get_truncated_excerpt(self, obj):
        # truncate the excerpt field
        return (
            obj.excerpt[: self.truncated_length] + "..."
            if len(obj.excerpt) > self.truncated_length
            else obj.excerpt
        )

    def get_truncated_description(self, obj):
        # truncate the description field
        return (
            obj.description[: self.truncated_length] + "..."
            if len(obj.description) > self.truncated_length
            else obj.description
        )

    def get_truncated_caption(self, obj):
        # truncate the caption field
        return (
            obj.caption[: self.truncated_length] + "..."
            if len(obj.caption) > self.truncated_length
            else obj.caption
        )

    def get_truncated_title(self, obj):
        # truncate the title field
        return (
            obj.title[: self.truncated_length] + "..."
            if len(obj.title) > self.truncated_length
            else obj.title
        )

    def get_truncated_name(self, obj):
        # truncate the name field
        return (
            obj.name[: self.truncated_length] + "..."
            if len(obj.name) > self.truncated_length
            else obj.name
        )

    def get_link_guid(self, obj):
        # create a link to the guid
        guid = obj.guid
        guid = f'<a href="{guid}" target="_blank">Open</a>'
        return mark_safe(guid)

    def get_link_link(self, obj):
        # create a link to the link
        link = obj.link
        link = f'<a href="{link}" target="_blank">Open</a>'
        return mark_safe(link)

    def get_link_source_url(self, obj):
        # create a link to the source_url
        source_url = obj.source_url
        source_url = f'<a href="{source_url}" target="_blank">Open</a>'
        return mark_safe(source_url)

    def create_wagtail_page(self, admin, request, queryset):
        for obj in queryset:
            result = Exporter(admin, request, obj).do_create_wagtail_page()
            print(result)

    def update_wagtail_page(self, admin, request, queryset):
        for obj in queryset:
            result = Exporter(admin, request, obj).do_update_wagtail_page()
            print(result)

    def clear_wagtail_page_id(self, admin, request, queryset):
        for obj in queryset:
            obj.wagtail_page_id = None
            obj.save()

    def export_wagtail_redirects(self, admin, request, queryset):
        """
        Export the wagtail redirects for the selected wordpress objects

        Only create redirects for objects that have a wagtail_page_id
        and the slug gerneated by wagtail does not match the slug in the wordpress object
        """

        # Delete all existing redirects, maybe this is a bit too much
        # but it's the easiest way to make sure we don't have any old redirects
        # TODO: Maybe we should only delete the redirects for the selected objects
        Redirect.objects.all().delete()

        for obj in queryset:
            if obj.wagtail_page_id:
                wagtail_page = Page.objects.get(id=obj.wagtail_page_id)
                if not obj.slug == wagtail_page.url_path.strip("/"):
                    Redirect.objects.create(
                        old_path=f"/{obj.slug}",
                        redirect_page_id=wagtail_page.id,
                        redirect_page_route_path=wagtail_page.url_path,
                        is_permanent=True,
                    )

        return True

    def get_actions(self, request):
        # add the create_wagtail_page action to the list of actions
        # if the model has a TARGET_WAGTAIL_PAGE_MODEL attribute
        actions = super().get_actions(request)
        if hasattr(self.model, "WAGTAIL_PAGE_MODEL"):
            actions["create_wagtail_page"] = (
                self.create_wagtail_page,
                "create_wagtail_page",
                "Create Wagtail Page",
            )
            actions["clear_wagtail_page_id"] = (
                self.clear_wagtail_page_id,
                "clear_wagtail_page_id",
                "Clear Wagtail Page ID",
            )
            actions["update_wagtail_page"] = (
                self.update_wagtail_page,
                "update_wagtail_page",
                "Update Wagtail Page",
            )
            actions["export_wagtail_redirects"] = (
                self.export_wagtail_redirects,
                "export_wagtail_redirects",
                "Export Wagtail Redirects",
            )
        return actions

    # set the column names
    get_truncated_content.short_description = "Content"
    get_truncated_excerpt.short_description = "Excerpt"
    get_truncated_description.short_description = "Description"
    get_truncated_caption.short_description = "Caption"
    get_truncated_title.short_description = "Title"
    get_truncated_name.short_description = "Name"
    get_link_guid.short_description = "Guid"
    get_link_link.short_description = "Link"
    get_link_source_url.short_description = "Source Url"
    get_renamed_id.short_description = "Import ID"


import_admin.register(WPPage, BaseAdmin)
import_admin.register(WPCategory, BaseAdmin)
import_admin.register(WPTag, BaseAdmin)
import_admin.register(WPAuthor, BaseAdmin)
import_admin.register(WPPost, BaseAdmin)
import_admin.register(WPComment, BaseAdmin)
import_admin.register(WPMedia, BaseAdmin)
