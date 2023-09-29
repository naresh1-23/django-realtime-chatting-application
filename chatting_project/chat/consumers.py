
from user.models import User
from . import models
import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def save_message(self,message, sender, receiver, room_id):
        room = models.Room.objects.filter(id = int(room_id)).first()
        msg_from = User.objects.filter(username = sender).first()
        msg_to = User.objects.filter(username = receiver).first()
        message = models.Chat.objects.create(message = message,room = room, msg_from = msg_from, msg_to = msg_to)
        message.save()
        print("saved")
        
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        sender = text_data_json["sender"]
        receiver = text_data_json["receiver"]
        room_id = self.room_name
        await self.save_message(message, sender, receiver, room_id)
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message, "sender": sender}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        sender = event["sender"]
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message, "sender": sender}))
        
        