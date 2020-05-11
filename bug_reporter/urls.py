from django.urls import include,path
from rest_framework.urlpatterns import format_suffix_patterns
from bug_reporter import views
from django.conf import settings
from django.conf.urls.static import static
# from bug_reporter import routers
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("",views.UserList.as_view(),name = "user-list"),
    path('users',views.UserList.as_view()),
    path('projects',views.ProjectList.as_view(),name = "project1-list"),
    path('project/<int:pk>/',views.ProjectDetail.as_view(),name = 'project-detail'),
    path('userpage/<int:pk>/',views.UserPage.as_view(),name = "user-page"),
    path('user/<int:pk>/',views.UserDetail.as_view(),name = "user-detail"),
    path('comment/',views.CommentDetail.as_view(),name = "comment-detail"),
    # path('bugs',views.BugList.as_view(),name = "bug-list"),
    path("bug/<int:pk>/",views.BugDetail.as_view(),name="bug-detail"),
    # path('sign_up/', views.SignUp.as_view(), name="sign_up"),    
    path('images/',views.ImageList.as_view(),name="Image_list"),
    path('project/{issueid}/bugs/',views.BugList.as_view(),name="project_views"),
    # path('api-token-auth/', obtain_auth_token),

]
# urlpatterns += routers.router.urls

urlpatterns = format_suffix_patterns(urlpatterns)

# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)