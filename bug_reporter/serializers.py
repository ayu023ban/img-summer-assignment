from rest_framework import serializers
from bug_reporter import models



class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model= models.Project
        fields=['name','wiki','users']
        extra_kwargs = {'users': {'required': False}}

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        models = models.Images
        fields = "__all__"

class BugSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    class Meta:
        model= models.Bug
        fields = ['project','user','name','description','tag','status',"images"]

class UserSerializer(serializers.ModelSerializer):
    many = True
    class Meta:
        model = models.User
        fields = ['username','githublink','isAdmin']

class UserPageSerializer(serializers.ModelSerializer):
    many=True
    projects = ProjectSerializer(many = True,read_only = True)
    bugs = BugSerializer(many = True,read_only = True)
    class Meta:
        model= models.User
        fields = ['username','githublink','isAdmin',"projects","bugs"]
        extra_kwargs = {'projects': {'required': False}}

class ProjectDetailSerializer(serializers.ModelSerializer):
    bugs = BugSerializer(many =True,read_only = True)
    class Meta:
        model = models.Project
        fields = ['name','wiki','users','bugs']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model= models.Comment
        fields = ['description','created_at','bug']

