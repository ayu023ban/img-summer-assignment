from rest_framework import generics, status, viewsets ,request
from rest_framework.parsers import FileUploadParser,MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
from bug_reporter.permissions import *
from bug_reporter import models , serializers
from django.http import Http404
from django_filters import rest_framework as filters
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from django.urls import path
# from django.db.models.signals import *

# Create your views here.
class UserList(generics.ListAPIView):
    # permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    authentication_classes = [SessionAuthentication,BasicAuthentication]
    # authentication_classes = [TokenAuthentication]
    permission_classes = [CustomAuthentication]
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    # def create(self, request, *args, **kwargs):
        
    #     return super().create(request, *args, **kwargs)


# for user in models.User.objects.all():
#     Token.objects.get_or_create(user=user)

# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    permission_classes = [CustomAuthentication,IsOwnerOfUserOrReadOnly]
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

class UserPage(generics.RetrieveAPIView):
    permission_classes = [CustomAuthentication]
    queryset = models.User.objects.all() 
    serializer_class= serializers.UserPageSerializer

class ProjectList(generics.ListCreateAPIView):
    permission_classes = [CustomAuthentication]
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer
    def perform_create(self, serializer):
        users = serializer.validated_data["users"]
        if self.request.user not in list(users):
            users.append(self.request.user)
        serializer.save(creator = self.request.user,users = users)

class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectDetailSerializer
    permission_classes = (CustomAuthentication,IsTeamMember,IsCreatorOfProject)


# class ProjectUpdate(generics.UpdateAPIView):
#     queryset = models.Project.objects.all()
#     serializer_class = serializers.ProjectDetailSerializer()
#     permission_classes = (IsTeamMember,)


class CommentDetail(generics.ListCreateAPIView):
    queryset=models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    
class BugList(generics.ListCreateAPIView):
    parser_classes = [MultiPartParser]
    queryset = models.Bug.objects.all()
    serializer_class = serializers.BugSerializer


    def perform_create(self, serializer,issueid):
        data = list(self.request.query_params)
        print(data,issueid)
        serializer.save(user=self.request.user)


    # def post(self, request, *args, **kwargs):
    #     print(request.data)
    #     project = models.Project.objects.get(pk=request.data["project"])
    #     new_bug = models.Bug.objects.create(project=project, user=user, name=request.data["name"], description=request.data["description"], tag=request.data["tag"], status = request.data["status"])
    #     # for image in images.values():
    #     # models.Images.objects.create(image = request.data["file"],bug=new_bug,comment = None)
    #     image_data = {"bug":new_bug,"comment":None,"image": request.data["image_upload"]}
    #     print(image_data)
    #     imageserial = serializers.ImageSerializer(data = image_data)
    #     if imageserial.is_valid():
    #         imageserial.save()
    #     return Response(data = request.data)

class ImageList(generics.ListCreateAPIView):
    parser_classes = [MultiPartParser]     
    queryset = models.Images.objects.all()
    serializer_class = serializers.ImageSerializer

class BugDetail(generics.RetrieveUpdateAPIView):
    queryset = models.Bug.objects.all()
    serializer_class = serializers.BugSerializer


# class SignUp(generics.CreateAPIView):
#     queryset = models.User.objects.all()
#     serializer_class = serializers.SignUpSerializer
#     permission_classes = (IsAuthenticatedOrCreate,)


# class ProjectViewSet(viewsets.ModelViewSet):
#     queryset = models.Project.objects.all()
#     serializer_class = serializers.ProjectSerializer
#     filter_backends = (filters.DjangoFilterBackend,)
#     filterset_fields = ['created_at']

# class BugViewSet(viewsets.ModelViewSet):
#     queryset = models.Bug.objects.all()
#     serializer_class = serializers.BugSerializer
#     # @action(method = ['post'])
#     def create(self,request):
#         serializer = serializers.BugSerializer(data = request.data)
#         if(serializer.is_valid()):
            
#             bugData = {"project":request.data["project"],"user":request.data["user"],"name":request.data["name"],"tag":request.data["tag"],"status":request.data["status"]}
#             bugSerializer = serializers.BugSerializer(data = bugData)
#             bugSerializer.save()            
#             print(bugData)
#             print(request.data)
#             imageSerializer = serializers.ImageSerializer(data = [])
#             return Response(data=request.data)
#         return Response(data=serializer.errors,status = status.HTTP_400_BAD_REQUEST)