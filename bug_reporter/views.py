import requests ,json.decoder ,json
from rest_framework import generics, status, viewsets ,request
from rest_framework.parsers import FileUploadParser,MultiPartParser
from rest_framework.decorators import permission_classes ,action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from bug_reporter.permissions import *
from bug_reporter import models , serializers
from django_filters import rest_framework as filters
from django.shortcuts import get_object_or_404
from django.http import HttpResponse , JsonResponse
import django_filters.rest_framework

# Create your views here.
class UserList(generics.ListAPIView):
    # permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    # authentication_classes = [SessionAuthentication,BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [CustomAuthentication]
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

class Login_with_temporary_token(generics.GenericAPIView) :
    queryset=models.User.objects.all()
    serializer_class=serializers.UserSerializer
    # lookup_field='code'
    # lookup_url_kwarg = 'code'
    def post(self,request):
        try:
            code = request.data["code"]
        except KeyError:
            return Response("'error' key is missing")
        post_data_for_token={
            "client_id":"l1Wb17BXy5ZoQeJ1fzOtZutOObUrzSi9fW1xxLGR",
            "client_secret":"lSHHesPe3SgiYsiB0PH2Bobpmsr0LZtnEtS1K3fa4m2HJwUrmIFSnrWNSSLkEbh5Sgzs0KOx4QIV9aq0wgtvy7Jlzf5SXjOrjgbqA8UWwZiXY67OPT6AO2oB8i7xVvnQ",
            "grant_type":"authorization_code",
            "redirect_url":"http://localhost:8000/bug_reporter/login/",
            "code":code
        }
        response= requests.post('https://internet.channeli.in/open_auth/token/', data=post_data_for_token).json()
        
        try:
            access_token = response["access_token"]
        except KeyError:
            return Response("Your code is Wrong")
        # print(access_token)
        headers = {
            'Authorization': 'Bearer ' + access_token,
        }
        user_data = requests.get(url="https://internet.channeli.in/open_auth/get_user_data/", headers=headers).json()
        # return JsonResponse(user_data)
        roles = user_data["person"]['roles']
        maintainer = False
        for i in roles:
            if i['role']=='Maintainer':
                maintainer = True
        if maintainer:
            try:
                user = models.User.objects.get(email=user_data['contactInformation']['instituteWebmailAddress'])
                response = self.login(user,response,user_data)
            except models.User.DoesNotExist:
                user = models.User(
                    username=user_data['person']['fullName'],
                    enroll_no=user_data['student']['enrolmentNumber'],
                    email=user_data['contactInformation']['instituteWebmailAddress'],
                    first_name =user_data['person']['fullName']
                )
                user.save()
                response = self.login(user,response,user_data)
        else:
             return HttpResponse("not Imgian")
        return HttpResponse(response)


    def login(self,user,access_response,user_data):
        try:
            auth_token = models.AuthToken.objects.get(user=user)
            auth_token.access_token=access_response["access_token"]
            auth_token.revoke_token=access_response["refresh_token"]
            auth_token.expires_in =  access_response["expires_in"]

        except models.AuthToken.DoesNotExist:
            auth_token = models.AuthToken(
                access_token=access_response["access_token"],
                revoke_token=access_response["refresh_token"],
                expires_in = access_response["expires_in"],
                user = user
            )
        try:
            token = Token.objects.get(user=user)
            token.delete()
            token = Token.objects.create(user=user)
        except Token.DoesNotExist:
            token = Token.objects.create(user=user)
        auth_token.pseudo_token = token
        auth_token.save()
        res = {
            "token":token.key,
            "user_data": user_data
        }
        return JsonResponse(res)


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
    # permission_classes ``= [CustomAuthentication]
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
    
class ImageList(generics.ListCreateAPIView):
    parser_classes = [MultiPartParser]     
    queryset = models.Images.objects.all()
    serializer_class = serializers.ImageSerializer

# class BugDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = models.Bug.objects.all()
#     serializer_class = serializers.BugUpdateSerializer

class BugViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser]
    queryset = models.Bug.objects.all()
    serializer_class = serializers.BugSerializer
    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
    __basic_fields = ['tag','issued_at','status','important']
    filter_fields= __basic_fields
    search_fields=__basic_fields
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.BugSerializer
        else:
            return serializers.BugUpdateSerializer
