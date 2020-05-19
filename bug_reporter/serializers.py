from rest_framework import serializers
from bug_reporter import models
from rest_framework.parsers import FileUploadParser,MultiPartParser

class ProjectSerializer(serializers.ModelSerializer):
    member_names = serializers.StringRelatedField(many=True,read_only=True,source='members')
    class Meta:
        model = models.Project
        fields = ['id','name', 'wiki',"member_names" ,'members','creator','created_at']
        read_only_fields=['id','created_at','creator',"member_names"]
        extra_kwargs = {'members': {'required': False}}

        def __str__(self):
            return self.name


class BugSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source = 'project.name')
    class Meta:
        model = models.Bug
        # fields='__all__'
        fields=('creator','description','important','issued_at','name','status','tag','project_name')
        extra_kwargs = {"creator":{"read_only":True}}



class BugUpdateSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source = 'project.name')
    class Meta:
        model = models.Bug
        fields = ['project','project_name', 'creator', 'name',
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
