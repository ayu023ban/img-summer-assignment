import requests
import json.decoder
import json
from rest_framework import generics, status, viewsets, request, mixins
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.decorators import permission_classes, action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from bug_reporter.permissions import *
from bug_reporter import models, serializers
from django_filters import rest_framework as filters
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponse, JsonResponse, Http404
import django_filters.rest_framework
from datetime import timedelta
from django.utils import timezone
from django.db.models import Q
import os
from django.conf import settings
file_path = os.path.join(settings.BASE_DIR, "bug_reporter/secret.txt")

secret = open(file_path, "r")


def expires_in(token):
    time_elapsed = timezone.now() - token.created
    left_time = timedelta(seconds=20*(60*60*24)) - time_elapsed
    return left_time


def is_token_expired(token):
    return expires_in(token) < timedelta(seconds=0)
# Create your views here.


class CommentViewSet(viewsets.ModelViewSet):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    filter_backends = (filters.DjangoFilterBackend,
                       SearchFilter, OrderingFilter)
    __basic_fields = ['bug', 'creator', 'description']
    filter_fields = __basic_fields
    search_fields = __basic_fields
    permission_classes_by_action = {'update': [CustomAuthentication, IsCreatorOfObject],
                                    'destroy': [CustomAuthentication, IsCreatorOfObject],
                                    'default': [CustomAuthentication]}

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError as e:
            return [permission() for permission in self.permission_classes_by_action['default']]

    def perform_create(self, serializer):
        comment = serializer.save(creator=self.request.user)
        creator = comment.creator.full_name
        bug = comment.bug
        bug_creator = bug.creator
        email = [bug_creator.email]
        subject = f"{creator} commented on your issue {bug.name}"
        message = f"<pre>{creator} commented on your issue {bug.name}.\nThe Comment is:</pre>"
        html_message = message+comment.description
        # send_mail(subject, message, settings.EMAIL_HOST_USER, email,
        #   fail_silently=True, html_message=html_message)


class UserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = models.User.objects.all()
    permission_classes_by_action = {'update': [CustomAuthentication, IsCreatorOfObject],
                                    'destroy': [CustomAuthentication, IsMaster],
                                    'login_with_temporary_token': [AllowAny],
                                    'loginWithCookie': [AllowAny],
                                    'disable': [IsMaster],
                                    'master': [IsMaster],
                                    'default': [CustomAuthentication],
                                    }

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError as e:
            return [permission() for permission in self.permission_classes_by_action['default']]

    def get_serializer_class(self):
        if self.request.method == "PUT" or self.request.method == "PATCH":
            return serializers.UserUpdateSerializer
        return serializers.UserSerializer

    @action(methods=['POST', 'OPTIONS'], detail=False, url_name='login', url_path='login')
    def login_with_temporary_token(self, request):
        try:
            code = request.data["code"]
        except KeyError:
            return Response("'error' key is missing", status=status.HTTP_404_NOT_FOUND)
        post_data_for_token = {
            "client_id": "l1Wb17BXy5ZoQeJ1fzOtZutOObUrzSi9fW1xxLGR",
            "client_secret": secret.readline(),
            "grant_type": "authorization_code",
            "redirect_url": "http://localhost:8000/bug_reporter/login/",
            "code": code
        }
        response = requests.post(
            'https://internet.channeli.in/open_auth/token/', data=post_data_for_token).json()

        try:
            access_token = response["access_token"]
        except KeyError:
            return Response("Your code is Wrong", status=status.HTTP_400_BAD_REQUEST)
        headers = {
            'Authorization': 'Bearer ' + access_token,
        }
        user_data = requests.get(
            url="https://internet.channeli.in/open_auth/get_user_data/", headers=headers).json()
        roles = user_data["person"]['roles']
        maintainer = True
        for i in roles:
            if i['role'] == 'Maintainer':
                maintainer = True
        if maintainer:
            try:
                user = models.User.objects.get(
                    email=user_data['contactInformation']['instituteWebmailAddress'])
                response = self.login(user, response, user_data)
            except models.User.DoesNotExist:
                first_name = user_data['person']['fullName'].split(" ")[0]
                last_name = user_data['person']['fullName'].split(" ")[1]
                user = models.User(
                    username=first_name+"_"+last_name,
                    enroll_no=user_data['student']['enrolmentNumber'],
                    email=user_data['contactInformation']['instituteWebmailAddress'],
                    first_name=first_name,
                    last_name=last_name,
                    full_name=user_data['person']['fullName']
                )
                user.save()
                response = self.login(user, response, user_data)
        else:
            return Response("not Imgian", status=status.HTTP_401_UNAUTHORIZED)
        return Response(response, status=status.HTTP_202_ACCEPTED)

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
            if is_token_expired(token):
                token.delete()
                token = Token.objects.create(user=user)
        except Token.DoesNotExist:
            token = Token.objects.create(user=user)
        auth_token.pseudo_token = token
        auth_token.save()
        res = {
            "token": token.key,
            "expires_in": expires_in(token),
            "user_data": serializers.UserSerializer(user).data
        }
        return res

    @action(methods=['GET'], detail=False, url_name='logout', url_path='logout')
    def logout(self, request):
        user = request.user
        auth_token = models.AuthToken.objects.get(user=user)
        token = Token.objects.get(user=user)
        auth_token.delete()
        token.delete()
        return Response("logged_out successfully", status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=False, url_name="CookieLogin", url_path="cookielogin")
    def loginWithCookie(self, request):
        try:
            token = request.data["token"]
        except KeyError:
            return Response("'error' token is missing", status=status.HTTP_404_NOT_FOUND)
        try:
            tokenModel = Token.objects.get(key=token)
        except Token.DoesNotExist:
            return Response("'error' your token is not valid", status=status.HTTP_404_NOT_FOUND)
        user = tokenModel.user
        res = {
            "token": token,
            "expires_in": expires_in(tokenModel),
            "user_data": serializers.UserSerializer(user).data
        }
        return Response(res)

    @action(methods=["GET"], detail=True, url_name="Disable", url_path="disable")
    def disable(self, request, pk):
        user = models.User.objects.get(pk=pk)
        user.isDisabled = not user.isDisabled
        user.save()
        ser = serializers.UserSerializer(user)
        return Response(ser.data)

    @action(methods=["GET"], detail=True, url_name="Master", url_path='master')
    def master(self, request, pk):
        user = models.User.objects.get(pk=pk)
        user.isMaster = not user.isMaster
        user.save()
        ser = serializers.UserSerializer(user)
        return Response(ser.data)


class BugViewSet(viewsets.ModelViewSet):
    queryset = models.Bug.objects.all().order_by('-issued_at')
    serializer_class = serializers.BugSerializer
    filter_backends = (filters.DjangoFilterBackend,
                       SearchFilter, OrderingFilter)
    __basic_fields = ['tags', 'creator', 'domain', 'status', 'important']
    filter_fields = __basic_fields
    search_fields = __basic_fields
    permission_classes_by_action = {'update': [CustomAuthentication, IsCreatorOfObject],
                                    'destroy': [CustomAuthentication, IsCreatorOfObject],
                                    'assign_bug': [CustomAuthentication, IsMemberOfProjectOfCurrentIssue],
                                    'default': [CustomAuthentication]}

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError as e:
            return [permission() for permission in self.permission_classes_by_action['default']]

    def perform_create(self, serializer):
        tags = self.request.data["tags"]
        bug = serializer.save(creator=self.request.user, status="P")
        for x in tags:
            (tag, _) = models.Tag.objects.get_or_create(name=x)
            tag.bugs.add(bug)

        project = bug.project
        members = project.members.all()
        emails = []
        for x in members:
            emails.append(x.email)
        subject = f"New Issue To Your Project {project.name}"
        message = "<p>A new issue is added to you project</p><p>Here is the description of the issue.</p><hr/><br/><br/>"
        html_message = message+bug.description
        # send_mail(subject, message, settings.EMAIL_HOST_USER, emails,
        #         fail_silently=False, html_message=html_message)

    @action(methods=['get', ], detail=True, url_path='assign', url_name='assign')
    def assign_bug(self, request, pk):
        assign_to = self.request.query_params.get('assign_to')
        if assign_to == 'None':
            assign_to = None
        bug = models.Bug.objects.get(pk=pk)

        if assign_to == None or models.User.objects.get(pk=assign_to) in bug.project.members.all():
            ser = serializers.BugSerializer(
                bug, data={'assigned_to': assign_to}, partial=True)
            if ser.is_valid():
                ser.save()
                return Response(ser.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'Error': 'User not a team member'}, status=status.HTTP_406_NOT_ACCEPTABLE)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = models.Project.objects.all().order_by('-created_at')
    serializer_class = serializers.ProjectSerializer
    filter_backends = (filters.DjangoFilterBackend,
                       SearchFilter, OrderingFilter)
    __basic_fields = ['name', 'wiki', 'githublink', 'creator', 'members']
    filter_fields = __basic_fields
    search_fields = __basic_fields
    permission_classes_by_action = {'update': [CustomAuthentication, IsTeamMember],
                                    'destroy': [CustomAuthentication, IsCreatorOfObject],
                                    'update_members': [CustomAuthentication, IsTeamMember],
                                    'default': [CustomAuthentication]}

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError as e:
            return [permission() for permission in self.permission_classes_by_action['default']]

    def perform_create(self, serializer):
        users = serializer.validated_data.get("members", [])
        if self.request.user.id not in list(users):
            users.append(self.request.user.id)
        serializer.save(creator=self.request.user, members=users)

    @action(methods=['patch'], detail=True, url_path='update_members', url_name='update_members')
    def update_members(self, request, pk):
        users = list(self.request.data.get("members", []))
        instance = self.get_object()
        creator_id = instance.creator.id
        if self.request.user.id not in list(users):
            users.append(self.request.user.id)
        if creator_id not in list(users):
            users.append(creator_id)
        project = models.Project.objects.get(pk=pk)
        ser = serializers.ProjectSerializer(
            project, data={"members": users}, partial=True)
        if ser.is_valid():
            ser.save()
            return Response({"status": "updated members successfully", "user_ids": users}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(ser.errors(), status=status.Http404)


class ImageViewSet(viewsets.ModelViewSet):
    queryset = models.Image.objects.all()
    serializer_class = serializers.ImageSerializer
    permission_classes = ([CustomAuthentication])
