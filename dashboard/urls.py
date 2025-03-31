from django.urls import path

from . import views

urlpatterns = [
    path("", views.redirect_to_dashboard, name='redirect_root'),
    path("dashboard/", views.index, name="dashboard"),
    path("information/", views.info, name="info")
    path("admin/", views.index , name="admin_pannel"),
]