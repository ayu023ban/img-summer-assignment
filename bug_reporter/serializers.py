from rest_framework import serializers
from bug_reporter import models
from rest_framework.parsers import FileUploadParser,MultiPartParser

class ProjectSerializer(serializers.ModelSerializer):
    member_names = serializers.StringRelatedField(many=True,read_only=True,source='members')
    no_of_issues = serializers.SerializerMethodField(read_only=True)
    def get_no_of_issues(self,obj):
        return obj.bugs.count()
    class Meta:
        model = models.Project
        fields ='__all__'
        read_only_fields=['id','created_at','creator',"member_names"]
        extra_kwargs = {'members': {'required': False}}

        def __str__(self):
            return self.name


class BugSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source = 'project.name', read_only=True)
    creator_name = serializers.CharField(source = 'creator.full_name',read_only=True)
    assigned_name = serializers.CharField(source = 'assigned_to.full_name',read_only=True,default=None)
    no_of_comments = serializers.SerializerMethodField(read_only=True)
    tags = serializers.SerializerMethodField()
    class Meta:
        model = models.Bug
        fields='__all__'
        read_only_fields = ['creator','issued_at','id','project_name','no_of_comments']

    def get_no_of_comments(self,obj):
        return obj.comments.count()
    def get_tags(self,obj):
        tags = obj.tags.all()
        print(tags)
        result = []
        for x in tags:
            result.append(x.name)
        return result


class UserSerializer(serializers.ModelSerializer):
    def get_no_of_projects(self,obj):
        return obj.projects.count()
    def get_no_of_issues(self,obj):
        return obj.bugs.count()
    no_of_projects = serializers.SerializerMethodField(read_only=True)
    no_of_issues = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.User
        fields = ['id',"no_of_issues","full_name","no_of_projects","isMaster",'username', 'githubLink','facebookLink','instagramLink',"linkedinLink","socialEmail",
                   "first_name","last_name","enroll_no","email","isDisabled"]
        read_only_fields = ['githublink','facebookLink','id','isMaster','instagramLink',"socialEmail","linkedinLink"]

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ["githubLink","username","first_name","last_name","full_name","facebookLink","instagramLink","linkedinLink","socialEmail"]


class CommentSerializer(serializers.ModelSerializer):
    creator_name = serializers.CharField(source='creator.full_name',read_only=True)
    class Meta:
        model = models.Comment
        fields = ['id','description', 'created_at','bug','creator',"creator_name"]
        read_only_fields=['creator','created_at',"creator"]
        extra_kwargs = {'bug': {'required':False}}

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields='__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = '__all__'