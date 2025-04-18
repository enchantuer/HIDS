from django.urls import re_path
from api.consumers import AlertConsumer, StatConsumer  # Le WebSocket Consumer

websocket_urlpatterns = [
    # re_path(r'ws/alerts/(?P<nb_of_alerts>\d+)?/?$', AlertConsumer.as_asgi()),
    re_path(r'ws/alerts/$', AlertConsumer.as_asgi()),
    re_path(r'ws/stats/$', StatConsumer.as_asgi()),
]
