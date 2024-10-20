from django.urls import path

import wp_connector


urlpatterns = [
    path("", wp_connector.urls),
]
