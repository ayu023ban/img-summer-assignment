from rest_framework import serializers
from bug_reporter import models
from rest_framework.parsers import FileUploadParser,MultiPartParser

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Project
        fields = ['id','name', 'wiki', 'members','creator','created_at']
        read_only_fields=['id','created_at','creator']
        extra_kwargs = {'members': {'required': False}}

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Images
        fields = "__all__"


class BugSerializer(serializers.ModelSerializer):
    # issued_at = serializers.DateTimeField(format="iso-8601", required=False, read_only=True)

    class Meta:
        model = models.Bug
        # fields = ['project', 'creator', 'name',
        #           'description', 'tag', 'status','issued_at']
        fields='__all__'
        extra_kwargs = {"creator":{"read_only":True}}


class BugUpdateSerializer(serializers.ModelSerializer):
    # images = ImageSerializer(source = "image_set",many =True,read_only = True)
    parser_classes = [FileUploadParser,MultiPartParser]
    class Meta:
        model = models.Bug
        fields = ['project', 'creator', 'name',
                  'description', 'tag', 'status',"issued_at","important"]
        extra_kwargs = {"user":{"read_only":True},"project":{"read_only":True}}


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id','username', 'githublink',
                   "first_name","enroll_no","email"]

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ["githublink"]

class ProjectDetailSerializer(serializers.ModelSerializer):
    bugs = BugSerializer(many=True, read_only=True)

    class Meta:
        model = models.Project
        fields = ['name', 'wiki', 'users', 'bugs']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ['description', 'created_at','bug','creator']
        extra_kwargs = {'bug': {'read_only':True},'creator': {'read_only':True}}
