from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_pannel, name='pannel'),
    path('', views.admin_pannel, name='admin_pannel'),
    path('utilisateurs/', views.utilisateurs, name='utilisateurs'),
    path('agents/', views.agents_page, name='agents'),

    path('verification/', views.verification, name='verification'),

    path('add_user/', views.add_user, name='add_user'),
    path('verify_old_password/', views.verify_old_password, name='verify_old_password'),
    path('check_email_exists/', views.check_email_exists, name='check_email_exists'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('get_user_counts/', views.get_user_counts, name='get_user_counts'),
    path('add_agent/', views.add_agent, name='add_agent'),
    path('delete_agent/<int:agent_id>/', views.delete_agent, name='delete_agent'),
    path('get_agent_counts/', views.get_agent_counts, name='get_agent_counts'),
]
