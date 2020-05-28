from django.db import models
from djrichtextfield.models import RichTextField
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.utils import timezone
# Create your models here.
class User(AbstractUser):
    def __str__(self):
        return self.username
    githublink = models.URLField(max_length=200 , blank=True,null=True)
    isMaster = models.BooleanField(default=False)
    isDisabled = models.BooleanField(default=False)
    enroll_no = models.IntegerField(default = 0)
    facebookLink = models.URLField(max_length=200,blank=True,null=True)
    instagramLink = models.URLField(max_length=200,blank=True,null=True)
    socialEmail = models.EmailField(max_length=200,blank=True,null=True)
    linkedinLink = models.URLField(max_length=200 ,blank=True,null=True)

class AuthToken(models.Model):
    access_token = models.CharField(max_length=40)
    revoke_token = models.CharField(max_length=40)
    expires_in = models.IntegerField()
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    pseudo_token = models.OneToOneField(Token, on_delete=models.SET_NULL,blank=True,null=True)
    

class Project(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=100)
    wiki = RichTextField(blank=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name = "projects",blank=True)
    created_at= models.DateTimeField("Creation Time",auto_now_add = True)
    githublink=models.URLField(max_length=200,blank=True,null=True)

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
    description = models.CharField(max_length=200,blank = True)
    issued_at = models.DateTimeField("Creation Time",auto_now_add = True)
    tag = models.CharField(max_length=100,blank=True,null=True)
    status = models.CharField(max_length=100,choices = STATUS_CHOICES)
    important = models.BooleanField(default=False)
    assigned_to = models.ForeignKey(User,related_name="issues_assigned_to_users",on_delete=models.SET_NULL,null=True)
    domain = models.CharField(choices=(('f','frontend'),('b','backend'),('o','other')),max_length=100,null=True,blank=True)
    class Meta:
        ordering=['issued_at']

class Comment(models.Model):
    def __str__(self):
        return self.description
    description = RichTextField()
    created_at = models.DateTimeField(auto_now_add = True)
    creator = models.ForeignKey(User,related_name="comments", on_delete=models.CASCADE,blank=True)
    bug = models.ForeignKey(Bug,related_name = "comments", on_delete=models.CASCADE)
    

# class Images(models.Model):
#     image = models.ImageField("uploaded image",blank =True,null = True)
#     bug = models.ForeignKey("Bug", related_name = "images", on_delete=models.CASCADE,blank=True,null=True,default =True)
#     comment = models.ForeignKey("Comment",related_name = "images",on_delete = models.CASCADE,blank = True,null=True)
    
