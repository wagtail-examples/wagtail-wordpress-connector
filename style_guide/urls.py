from django.urls import path

from . import views

urlpatterns = [
    path("", views.style_guide_view, name="style-guide"),
]
