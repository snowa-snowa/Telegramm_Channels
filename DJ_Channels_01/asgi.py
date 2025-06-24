"""
ASGI config for DJ_Channels_01 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""


import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
import appone.routing  # импортируешь свой routing.py, если он есть

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DJ_Channels_01.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            appone.routing.websocket_urlpatterns
        )
    ),
})
