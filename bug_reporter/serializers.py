from rest_framework import serializers
from bug_reporter import models
from rest_framework.parsers import FileUploadParser,MultiPartParser

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Project
        fields = ['name', 'wiki', 'users','creator']
        extra_kwargs = {'users': {'required': False},'creator':{'read_only':True}}

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Images
        fields = "__all__"


class BugSerializer(serializers.ModelSerializer):
    # images = ImageSerializer(many=True)
    images = ImageSerializer(source="image_set", many=True, read_only=True)
    # image_upload = serializers.FileField(write_only = True)
    parser_classes = [FileUploadParser,MultiPartParser]
    # print(image_upload)
    class Meta:
        model = models.Bug
        fields = ['project', 'creator', 'name',
                  'description', 'tag', 'status', "images","issued_at"]
        extra_kwargs = {"user":{"read_only":True},"project":{"read_only":True}}
        # read_only_fields=["images"]

    # def create(self, validated_data):
        # images = self.context.get('view').request.image_upload
        # new_bug = models.Bug.objects.create(
        #     project=validated_data.get("project")
        #     , user=validated_data.get("user")
        #     , name=validated_data.get("name")
        #     , description=validated_data.get("description")
        #     , tag=validated_data.get("tag")
        #     , status = validated_data.get("status"))
        # for image in images.values():
        #     # models.Image.objects.create(image = image_upload,bug=new_bug,comment = None)
        #     imageserial = ImageSerializer(data = {"bug":new_bug,"comment":None,"image": validated_data.get("image_upload")})
        #     imageserial.save()

class BugUpdateSerializer(serializers.ModelSerializer):
    images = ImageSerializer(source = "image_set",many =True,read_only = True)
    parser_classes = [FileUploadParser,MultiPartParser]
    class Meta:
        model = models.Bug
        fields = ['project', 'creator', 'name',
                  'description', 'tag', 'status', "images"]
        extra_kwargs = {"user":{"read_only":True},"project":{"read_only":True}}


class UserSerializer(serializers.ModelSerializer):
    many = True

    class Meta:
        model = models.User
        fields = ['username', 'githublink',
                   "first_name", "last_name"]


class UserPageSerializer(serializers.ModelSerializer):
    many = True
    projects = ProjectSerializer(many=True, read_only=True)
    bugs = BugSerializer(many=True, read_only=True)

    class Meta:
        model = models.User
        fields = ['username', 'githublink', "projects", "bugs"]
        extra_kwargs = {'projects': {'required': False}}


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


# class SignUpSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.User
#         fields = ["username", "password"]
#         extra_kwargs = {"password": {"write_only": True}}
