from vote.consumers import ws_add, ws_message, ws_disconnect

from django.urls import re_path

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

application = ProtocolTypeRouter({

    "websocket": AuthMiddlewareStack(
        URLRouter([
            re_path("websocket.connect", ws_add),
            re_path("websocket.receive", ws_message),
            re_path("websocket.disconnect", ws_disconnect),
        ])
    ),
})