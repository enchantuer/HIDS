from django.urls import path

from . import views

urlpatterns = [
    path("agents", views.get_agents, name="api_agents"),
    path("alerts", views.get_alerts, name="api_alerts"),
    path("stats", views.get_stats, name="api_stats"),
]