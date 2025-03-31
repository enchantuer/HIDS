from django.urls import path

from . import views

urlpatterns = [
    path("", views.admin_pannel, name="admin_pannel"),
]