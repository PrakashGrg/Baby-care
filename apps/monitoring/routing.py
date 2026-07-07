from django.urls import re_path
from .consumers import MonitorConsumer

websocket_urlpatterns = [
    re_path(r'ws/monitor/(?P<room_name>\w+)/$', MonitorConsumer.as_asgi()),
]