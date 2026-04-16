import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from chats.models import Conversation, Participant


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope["url_route"]["kwargs"]["conversation_id"]
        self.room_group_name = f"chat_{self.conversation_id}"

        user = self.scope.get("user")

        # reject if not authenticated
        if not user or not user.is_authenticated:
            await self.close()
            return

        # validate user is part of conversation
        is_member = await self.is_user_in_conversation(user.id, self.conversation_id)
        if not is_member:
            await self.close()
            return

        # join group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        print(f"[WS CONNECT] Channel: {self.channel_name} | User: {user.email}")
        await self.accept()

        # broadcast online status
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "user_status",
                "user": user.email,
                "status": "online"
            }
        )

    async def disconnect(self, close_code):
        user = self.scope.get("user")
        if user and user.is_authenticated:
            # broadcast offline status
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "user_status",
                    "user": user.email,
                    "status": "offline"
                }
            )

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
        except Exception:
            return

        message_text = data.get("message")
        msg_type = data.get("type", "message")
        user = self.scope.get("user")

        if not user:
            return

        if msg_type == "ping":
            # Someone wants to know who is online, broadcast our status back
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "user_status",
                    "user": user.email,
                    "status": "online"
                }
            )
            return

        if not message_text:
            return

        # persist message
        message_obj = await self.save_message(user.id, self.conversation_id, message_text)
        print(f"[WS RECEIVE] From: {user.email} | Content: {message_text}")

        # broadcast
        print(f"[WS GROUP SEND] Room: {self.room_group_name} | Message ID: {message_obj['id']}")
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message_obj["content"],
                "user": message_obj["sender"],
                "message_id": message_obj["id"],
                "created_at": message_obj["created_at"],
            }
        )

    async def chat_message(self, event):
        print(f"[WS BROADCAST] Sending to {self.channel_name} | Content: {event['message']}")
        await self.send(text_data=json.dumps({
            "type": "message",
            "message": event["message"],
            "user": event["user"],
            "message_id": event["message_id"],
            "created_at": event["created_at"],
        }))

    async def user_status(self, event):
        await self.send(text_data=json.dumps({
            "type": "user_status",
            "user": event["user"],
            "status": event["status"]
        }))

    # ---------------- DB OPERATIONS ---------------- #

    @database_sync_to_async
    def is_user_in_conversation(self, user_id, conversation_id):
        return Participant.objects.filter(
            user_id=user_id,
            conversation_id=conversation_id
        ).exists()

    @database_sync_to_async
    def save_message(self, user_id, conversation_id, content):
        from messaging.models import Message

        message = Message.objects.create(
            sender_id=user_id,
            conversation_id=conversation_id,
            content=content,
            type="text",
        )

        return {
            "id": message.id,
            "content": message.content,
            "sender": message.sender.email,
            "created_at": message.created_at.isoformat(),
        }