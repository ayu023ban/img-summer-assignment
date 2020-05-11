from django.db import models
from djrichtextfield.models import RichTextField
from django.contrib.auth.models import AbstractUser,AbstractBaseUser
from django.conf import settings
from rest_framework.authtoken.models import Token


# Create your models here.
class User(AbstractUser):
    def __str__(self):
        return self.username
    # username = models.CharField(max_length=100,blank=False)
    # email = models.CharField(max_length=100,blank=False)
    # password = models.CharField(max_length=100)
    # username = models.CharField(max_length = 200)
    githublink = models.URLField(max_length=200)
    isMaster = models.BooleanField(default=False)
    isDisabled = models.BooleanField(default=False)


class Project(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=100)
    wiki = RichTextField(blank=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name = "projects",blank=True)
    created_at= models.DateTimeField("Creation Time",auto_now_add = True)

class Bug(models.Model):
    STATUS_CHOICES=(
        ("P","Pending"),
        ("R","Resolved"),
        ("T","To be Discussed")
    )
    def __str__(self):
        return self.name
    project = models.ForeignKey(Project,related_name = "bugs", on_delete=models.CASCADE)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,related_name = "bugs", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = RichTextField(blank = True)
    # image = models.ImageField("uploaded image", blank=True,null = True)
    issued_at = models.DateTimeField(auto_now_add=True,blank=True)
    tag = models.CharField(max_length=100,blank=True,null=True)
    status = models.CharField(max_length=100,choices = STATUS_CHOICES)
    

class Comment(models.Model):
    def __str__(self):
        return self.description
    description = RichTextField()
    created_at = models.DateTimeField(auto_now_add = True)
    creator = models.ForeignKey(User,related_name="comments", on_delete=models.CASCADE,blank=True)
    bug = models.ForeignKey(Bug,related_name = "comments", on_delete=models.CASCADE)
    

class Images(models.Model):
    image = models.ImageField("uploaded image",blank =True,null = True)
    bug = models.ForeignKey("Bug", related_name = "images", on_delete=models.CASCADE,blank=True,null=True,default =True)
    comment = models.ForeignKey("Comment",related_name = "images",on_delete = models.CASCADE,blank = True,null=True)
    
