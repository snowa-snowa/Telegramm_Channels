# chat/routing.py

from django.urls import re_path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    # теперь в URL передаётся ID беседы
    re_path(r"ws/chat/(?P<convo_id>\d+)/$", ChatConsumer.as_asgi()),
]
