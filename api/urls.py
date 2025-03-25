from django.urls import path

from . import views

urlpatterns = [
    path("agents", views.get_agents, name="agents"),
    path("alerts", views.get_alerts, name="alerts"),
]