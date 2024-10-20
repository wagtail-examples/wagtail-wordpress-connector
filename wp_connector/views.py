from django.views.generic import RedirectView


def import_admin_redirect_view(request):
    return RedirectView.as_view(url="/import-admin/", permanent=False)(request)
