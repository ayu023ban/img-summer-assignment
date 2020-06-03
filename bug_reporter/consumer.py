import asyncio
import json
import inspect
import io
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import *
from .serializers import *
from rest_framework.authtoken.models import Token

class CommentConsumer(WebsocketConsumer):

    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["issue_id"]
        self.issue_id = int(self.room_name)
        self.room_group_name = "issue_"+self.room_name
        room_group_name = self.room_group_name
        async_to_sync(self.channel_layer.group_add)(
            room_group_name,
            self.channel_name
        )
        self.accept()


    def disconnect(self, close_code=None):
        self.send(json.dumps({"end_message":close_code}))
        async_to_sync (self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        self.close()

    def fetch_messages(self, data,user):
        issue = None
        try:
            issue = Bug.objects.get(pk = self.issue_id)
        except Bug.DoesNotExist:
            self.disconnect("issue does not exists")
        comments = issue.comments.all().order_by("-created_at")
        serialized_comment = CommentSerializer(comments,many=True).data
        content = JSONRenderer().render(serialized_comment)
        stream = io.BytesIO(content)
        data = JSONParser().parse(stream)
        data = {"command":"messages","data":data}
        self.send(text_data=json.dumps(data))
  

    def new_message(self, data,user):
        comment = ""
        try:
            comment = data["description"]
        except KeyError:
            self.disconnect("description key not available in data")
        bug = Bug.objects.get(pk=self.issue_id)
        new_comment = Comment.objects.create(description=comment,creator=user,bug=bug)
        serialized_comment = CommentSerializer(new_comment).data
        data = {"command":"new_message","data":serialized_comment}
        self.send_event(data)
      
    commands = {
        'fetch_messages' : fetch_messages,
        'new_message' : new_message
    }
    
    def check_token(self,json_data):
        try:
            token = json_data["token"]
        except KeyError:
            self.disconnect("token key not present")
            return "undefined"
        try:
            token_object = Token.objects.get(key=token)
        except Token.DoesNotExist:
            self.disconnect("invalid token. Token does not exists")
            return "undefined"
        user = token_object.user
        return user

    def receive(self, text_data):
        json_data = json.loads(text_data)
        user = self.check_token(json_data)
        if user != "undefined":
            try:
                command = json_data["command"]
                if command not in self.commands.keys():
                    self.disconnect("command property not valid")
            except KeyError:
                self.disconnect("command property is not present")
            self.commands[command](self,json_data,user)

    def send_event(self,data):
        string_data = json.dumps(data)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
            "type":"comment_message",
            "text":string_data
            }
            )

    def comment_message(self,event):
        self.send(text_data=event["text"])