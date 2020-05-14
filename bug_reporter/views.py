import requests ,json.decoder
from rest_framework.views import APIView
from rest_framework import generics, status, viewsets ,request
from rest_framework.parsers import FileUploadParser,MultiPartParser
from rest_framework.decorators import permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication,TokenAuthentication
from bug_reporter.permissions import *
from bug_reporter import models , serializers
from django_filters import rest_framework as filters
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

# Create your views here.
class UserList(generics.ListAPIView):
    # permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    authentication_classes = [SessionAuthentication,BasicAuthentication]
    # authentication_classes = [TokenAuthentication]
    permission_classes = [CustomAuthentication]
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

class Login_with_temporary_token(generics.GenericAPIView) :
    queryset=models.User.objects.all()
    serializer_class=serializers.UserSerializer
    # lookup_field='code'
    # lookup_url_kwarg = 'code'
    def get(self,request):
        code =request.query_params.get('code')
        post_data_for_token={
            "client_id":"mkxe5ns7lBOwM7RMVPITL90uiy9zi2CCAOX1chM9",
            "client_secret":"hX35FshO9Czl4ZQUnQs3QfdGbETc5Duy2QMu5oy4oHbwU4tmzK37tIngbBli3WkRZeFtE9kixrwpOWA6hA8ee1yecOf8D7wtkGGE17m5EGaUx4vxSn4ceJuOMhM2BBwi",
            "grant_type":"authorization_code",
            "redirect_url":"http://localhost:8000/bug_reporter/login/",
            "code":code
        }
        response= requests.post('https://internet.channeli.in/open_auth/token/', data=post_data_for_token).json()
        access_token = response["access_token"]
        
        headers = {
            'Authorization': 'Bearer ' + access_token,
        }
        user_data = requests.get(url="https://internet.channeli.in/open_auth/get_user_data/", headers=headers)
        return HttpResponse(user_data)


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
    permission_classes = (CustomAuthentication,IsTeamMember,IsCreatorOfObject)

class CommentDetail(generics.ListCreateAPIView):
    queryset=models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    def perform_create(self, serializer):
        bug = get_object_or_404(models.Bug,pk=self.kwargs["bugid"])
        serializer.save(creator=self.request.user,bug=bug)
    
class BugList(generics.ListCreateAPIView):
    parser_classes = [MultiPartParser]
    queryset = models.Bug.objects.all()
    serializer_class = serializers.BugSerializer

    def perform_create(self, serializer):
        project = get_object_or_404(models.Project,pk=self.kwargs["projectid"])
        serializer.save(project = project,creator=self.request.user)


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

class BugDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Bug.objects.all()
    serializer_class = serializers.BugUpdateSerializer
