import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.conf import settings
from rest_framework_simplejwt.backends import TokenBackend


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'

        token = self.get_token_from_scope()
        if not token:
            await self.close()
            return

        token_data = self.decode_token(token)
        if not token_data:
            await self.close()
            return

        self.user_id = token_data.get('user_id')
        self.user_role = token_data.get('role')

        # Admin has access to all rooms
        if self.user_role != 'admin':
            has_access = await self.check_room_access(self.room_id, self.user_id)
            if not has_access:
                await self.close()
                return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        content = data.get('message', '').strip()
        if not content:
            return

        room_status = await self.get_room_status(self.room_id)

        # Patients cannot send messages in pending rooms
        if self.user_role == 'patient' and room_status == 'pending':
            await self.send(text_data=json.dumps({
                'error': 'Waiting for the doctor to accept your request.',
            }))
            return

        # Nobody can send messages in rejected rooms
        if room_status == 'rejected':
            await self.send(text_data=json.dumps({
                'error': 'This conversation request was rejected.',
            }))
            return

        message = await self.save_message(self.room_id, self.user_id, content)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': content,
                'sender_id': self.user_id,
                'sender_email': message['sender_email'],
                'timestamp': message['timestamp'],
                'message_id': message['id'],
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender_id': event['sender_id'],
            'sender_email': event['sender_email'],
            'timestamp': event['timestamp'],
            'message_id': event['message_id'],
        }))

    def get_token_from_scope(self):
        query_string = self.scope.get('query_string', b'').decode()
        for part in query_string.split('&'):
            if part.startswith('token='):
                return part.split('=', 1)[1]
        return None

    def decode_token(self, token):
        try:
            backend = TokenBackend(algorithm='HS256', signing_key=settings.SECRET_KEY)
            return backend.decode(token, verify=True)
        except Exception:
            return None

    @database_sync_to_async
    def check_room_access(self, room_id, user_id):
        from .models import ChatRoom
        try:
            room = ChatRoom.objects.get(id=room_id)
            return (
                room.doctor.user_id == user_id or
                room.patient.user_id == user_id
            )
        except ChatRoom.DoesNotExist:
            return False

    @database_sync_to_async
    def get_room_status(self, room_id):
        from .models import ChatRoom
        try:
            room = ChatRoom.objects.get(id=room_id)
            return room.status
        except ChatRoom.DoesNotExist:
            return 'rejected'

    @database_sync_to_async
    def save_message(self, room_id, user_id, content):
        from .models import ChatRoom, ChatMessage
        from users.models import User
        room = ChatRoom.objects.get(id=room_id)
        sender = User.objects.get(id=user_id)
        msg = ChatMessage.objects.create(room=room, sender=sender, content=content)
        return {
            'id': msg.id,
            'sender_email': sender.email,
            'timestamp': msg.timestamp.isoformat(),
        }
