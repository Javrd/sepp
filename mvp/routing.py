# chat/routing.py
import os

from django.conf.urls import url

from . import consumers

https = os.getenv('HTTPS', 'False')=='True'
proto = 'wss' if https else 'ws'

websocket_urlpatterns = [
    url(r'^' + proto + r'/chat/(?P<room_name>[^/]+)/$', consumers.ChatConsumer),
]
