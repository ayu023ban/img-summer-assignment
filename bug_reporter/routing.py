from django.urls import re_path
from channels.routing import ProtocolTypeRouter,URLRouter
from bug_reporter.consumer import CommentConsumer
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator,OriginValidator
application = ProtocolTypeRouter({
    'websocket':
        AuthMiddlewareStack(
            URLRouter(
                [
                    re_path(r"ws/comments/(?P<issue_id>[^/]+)$",CommentConsumer)
                ]
            )
        )
    
})