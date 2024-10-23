from django.apps import apps
from wagtail.admin.panels import HelpPanel, Panel


class WordpressInfoPanel(HelpPanel):
    """
    Panel that displays information about the Wordpress page that is connected to the Wagtail page.

    Becuase the wagtail model has no direct relation to the wordpress model, the panel
    needs to be provided with the content of the wordpress model in the form of a string
    in the format "app_name.ModelName"

    The panel will then display the title of the wordpress page and a link to the admin page

    Example:
        WordpressInfoPanel(content="wp_connector.WPPage")
    """

    def __init__(
        self,
        heading="Wordpress Info",
        content=None,
        template="wp_connector/panels/wordpress_info_panel.html",
        **kwargs
    ):
        super().__init__(**kwargs)
        self.heading = heading
        self.content = content
        self.template = template

    class BoundPanel(Panel.BoundPanel):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.template_name = self.panel.template
            self.content = self.panel.content

            wp_model = apps.get_model(
                self.content.split(".")[0], self.content.split(".")[1]
            )
            instance = wp_model.objects.filter(wagtail_page_id=self.instance.pk).first()
            # import-admin/wp_connector/wppage/?q=[wagtail_page_id]
            instance_url = (
                "/import-admin/wp_connector/"
                + wp_model.__name__.lower()
                + "/?q="
                + str(instance.wagtail_page_id)
            )
            instance_title = instance.title

            self.instance_url = instance_url
            self.instance_title = instance_title
