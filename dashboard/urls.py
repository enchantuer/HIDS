from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="dashboard"),
    path("info", views.info, name="info")
]