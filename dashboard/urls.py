from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="dashboard"),
    path("admin/", views.index , name="admin_pannel"),
]