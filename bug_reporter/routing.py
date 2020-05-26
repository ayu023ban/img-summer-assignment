# mysite/routing.py
from django.urls import path, re_path
from django.conf.urls import url
from channels.routing import ProtocolTypeRouter,URLRouter
from bug_reporter.consumer import CommentConsumer
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator,OriginValidator
application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket':
        AuthMiddlewareStack(
            URLRouter(
                [
                    re_path(r"ws/comments/(?P<issue_id>[^/]+)$",CommentConsumer)
                ]
            )
        )
    
})
# from . import consumer
# (?P<issue_id>[^/]+)
# channel_routing = {
#     'websocket.connect': consumer.ws_connect,
#     # 'websocket.receive': consumer.ws_receive,
#     # 'websocket.disconnect': consumer.ws_disconnect,
# }