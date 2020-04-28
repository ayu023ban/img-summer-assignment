from django.urls import include,path
from rest_framework.urlpatterns import format_suffix_patterns
from bug_reporter import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("",views.UserList.as_view(),name = "user-list"),
    path('users',views.UserList.as_view()),
    path('projects',views.ProjectList.as_view(),name = "project1-list"),
    path('project/<int:pk>/',views.ProjectDetail.as_view(),name = 'project-detail'),
    path('userpage/<int:pk>/',views.UserPage.as_view(),name = "user-page"),
    path('user/<int:pk>/',views.UserDetail.as_view(),name = "user-detail"),
    path('comment/',views.CommentDetail.as_view(),name = "comment-detail"),
    path('bugs',views.BugList.as_view(),name = "bug-list"),
]

urlpatterns = format_suffix_patterns(urlpatterns)

# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)