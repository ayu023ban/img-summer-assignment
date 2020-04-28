from bug_reporter import models
from bug_reporter import serializers
from rest_framework import generics
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
# Create your views here.
class UserList(generics.ListCreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

class UserPage(generics.RetrieveAPIView):
    queryset = models.User.objects.all() 
    serializer_class= serializers.UserPageSerializer

class ProjectList(generics.ListCreateAPIView):
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer

class ProjectDetail(generics.RetrieveUpdateAPIView):
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectDetailSerializer
class CommentDetail(generics.ListCreateAPIView):
    queryset=models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    
class BugList(generics.ListCreateAPIView):
    queryset = models.Bug.objects.all()
    serializer_class = serializers.BugSerializer


