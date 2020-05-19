from django.urls import include,path
from rest_framework.urlpatterns import format_suffix_patterns
from bug_reporter import views
from django.conf import settings
from django.conf.urls.static import static
from bug_reporter import routers
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('bugs/<int:bugid>/comment/',views.CommentDetail.as_view(),name = "comment-detail"),
]
urlpatterns += routers.router.urls

urlpatterns = format_suffix_patterns(urlpatterns)

# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)