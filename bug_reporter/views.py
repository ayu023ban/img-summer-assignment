import requests
import json.decoder
import json
from rest_framework import generics, status, viewsets, request,mixins
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.decorators import permission_classes, action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated,AllowAny
from bug_reporter.permissions import *
from bug_reporter import models, serializers
from django_filters import rest_framework as filters
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse,Http404
import django_filters.rest_framework


# Create your views here.
class CommentDetail(generics.ListCreateAPIView):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes=[CustomAuthentication,IsOwnerOfUserOrReadOnly]
    def perform_create(self, serializer):
        bug = get_object_or_404(models.Bug, pk=self.kwargs["bugid"])
        serializer.save(creator=self.request.user, bug=bug)


class ImageList(generics.ListCreateAPIView):
    parser_classes = [MultiPartParser]
    queryset = models.Images.objects.all()
    serializer_class = serializers.ImageSerializer


class UserViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,viewsets.GenericViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

    def get_serializer_class(self):
        if self.request.method =="PUT":
            return serializers.UserUpdateSerializer
        return serializers.UserSerializer

    @action(methods=['POST', 'OPTIONS'], detail=False, url_name='login', url_path='login')
    @permission_classes([AllowAny])
    def login_with_temporary_token(self,request):
        try:
            code = request.data["code"]
        except KeyError:
            return Response("'error' key is missing")
        post_data_for_token = {
            "client_id": "l1Wb17BXy5ZoQeJ1fzOtZutOObUrzSi9fW1xxLGR",
            "client_secret": "lSHHesPe3SgiYsiB0PH2Bobpmsr0LZtnEtS1K3fa4m2HJwUrmIFSnrWNSSLkEbh5Sgzs0KOx4QIV9aq0wgtvy7Jlzf5SXjOrjgbqA8UWwZiXY67OPT6AO2oB8i7xVvnQ",
            "grant_type": "authorization_code",
            "redirect_url": "http://localhost:8000/bug_reporter/login/",
            "code": code
        }
        response = requests.post(
            'https://internet.channeli.in/open_auth/token/', data=post_data_for_token).json()

        try:
            access_token = response["access_token"]
        except KeyError:
            return Response("Your code is Wrong")
        headers = {
            'Authorization': 'Bearer ' + access_token,
        }
        user_data = requests.get(
            url="https://internet.channeli.in/open_auth/get_user_data/", headers=headers).json()
        roles = user_data["person"]['roles']
        maintainer = False
        for i in roles:
            if i['role'] == 'Maintainer':
                maintainer = True
        if maintainer:
            try:
                user = models.User.objects.get(
                    email=user_data['contactInformation']['instituteWebmailAddress'])
                response = self.login(user, response, user_data)
            except models.User.DoesNotExist:
                user = models.User(
                    username=user_data['person']['fullName'],
                    enroll_no=user_data['student']['enrolmentNumber'],
                    email=user_data['contactInformation']['instituteWebmailAddress'],
                    first_name=user_data['person']['fullName']
                )
                user.save()
                response = self.login(user, response, user_data)
        else:
             return HttpResponse("not Imgian")
        return HttpResponse(response)

    def login(self, user, access_response, user_data):
        try:
            auth_token = models.AuthToken.objects.get(user=user)
            auth_token.access_token = access_response["access_token"]
            auth_token.revoke_token = access_response["refresh_token"]
            auth_token.expires_in = access_response["expires_in"]

        except models.AuthToken.DoesNotExist:
            auth_token = models.AuthToken(
                access_token=access_response["access_token"],
                revoke_token=access_response["refresh_token"],
                expires_in=access_response["expires_in"],
                user=user
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
            "token": token.key,
            "user_data": user_data
        }
        return JsonResponse(res)

    @permission_classes([IsAuthenticated])
    def logout(self, request):
        user = request.user
        auth_token = models.AuthToken.objects.get(user=user)
        token = Token.objects.get(user=user)
        auth_token.delete()
        token.delete()
        return Response("logged_out successfully", status=status.HTTP_200_OK)

    
        

class BugViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser]
    queryset = models.Bug.objects.all()
    serializer_class = serializers.BugSerializer
    filter_backends = (filters.DjangoFilterBackend,
                       SearchFilter, OrderingFilter)
    __basic_fields = ['tag', 'issued_at', 'status', 'important']
    filter_fields = __basic_fields
    search_fields = __basic_fields
    permission_classes = [CustomAuthentication,IsOwnerOfUserOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
 
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.BugSerializer
        else:
            return serializers.BugUpdateSerializer

    @action(methods=['patch', ], detail=True, url_path='resolve', url_name='resolve')
    def resolve(self, request, pk):
        bug = models.Bug.objects.get(pk=pk)
        bug.resolved = True
        bug.save()
        ser = serializers.BugSerializer(bug)
        return Response(ser.data)

    @action(methods=['patch', ], detail=True, url_path='assign', url_name='assign')
    def assign_bug(self, request, pk):
        assign_to = self.request.query_params.get('assign_to')
        bug = models.Bug.objects.get(pk=pk)

        if models.User.objects.get(pk=assign_to) in bug.project.members.all():
            ser = serializers.BugSerializer(bug, data={'assigned_to': assign_to}, partial=True)
            if ser.is_valid():
                ser.save()
                return Response({'status': 'Assignment Successful'}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'Error': 'User not a team member'}, status=status.HTTP_406_NOT_ACCEPTABLE)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer
    permission_classes = [IsAuthenticated]
    permission_classes_by_action ={
        'update':[CustomAuthentication,IsTeamMember],
        'destroy':[CustomAuthentication,IsCreatorOfObject],
        'create`':[CustomAuthentication]
    }
    def perform_create(self, serializer):
        users = serializer.validated_data["members"]
        if self.request.user not in list(users):
            users.append(self.request.user)
        serializer.save(creator = self.request.user,members = users)


    @action(methods=['get', ], detail=True, url_path='bugs', url_name='bugs')
    def get_issues(self, request, pk):
        user = request.user
        try:
            bug_list = models.Bug.objects.filter(project=pk)
        except models.Bug.DoesNotExist:
            return Response({'Empty': 'No Bugs for this project yet'}, status=status.HTTP_204_NO_CONTENT)

        ser = serializers.BugSerializer(bug_list, many=True)
        return Response(ser.data)
    
    @action(methods=['get', ], detail=True, url_path='team', url_name='team')
    def get_team_members(self, request, pk):
        project = models.Project.objects.get(pk=pk)
        members_list = project.members
        ser = serializers.UserSerializer(members_list, many=True)
        return Response(ser.data)

