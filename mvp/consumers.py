# chat/consumers.py
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import User, Message
from datetime import datetime
import json


class ChatConsumer(WebsocketConsumer):
    def connect(self):

        principal = self.scope['user']
        contact = User.objects.get(
            id=self.scope['url_route']['kwargs']['room_name'])

        if principal.id > contact.id:
            self.room_name = str(contact.id)+'-'+str(principal.id)
        else:
            self.room_name = str(principal.id)+'-'+str(contact.id)
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message'].strip()

        # Save and send message to room group
        if message:

            principal = self.scope['user']
            contact = User.objects.get(
                id=self.scope['url_route']['kwargs']['room_name'])

            message = Message.objects.create(
                sender=principal, receiver=contact, timeStamp=datetime.now(), text=message)
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message.text,
                    'userId': message.sender.id,
                    'image': message.sender.logo.name,
                    'date': message.timeStamp.strftime("%d/%m/%Y %H:%M")
                }
            )

    # Receive message from room group
    def chat_message(self, event):
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': event['message'],
            'userId': event['userId'],
            'image': event['image'],
            'date': event['date']
        }))
