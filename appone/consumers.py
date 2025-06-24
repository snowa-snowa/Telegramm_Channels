import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message, Conversation

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # получаем ID беседы из URL
        self.convo_id = self.scope['url_route']['kwargs']['convo_id']
        self.group_name = f"conversation_{self.convo_id}"

        user = self.scope['user']
        # проверяем, что пользователь в беседе
        convo = await database_sync_to_async(Conversation.objects.get)(id=self.convo_id)
        members = await database_sync_to_async(lambda: list(convo.members.all()))()
        if not user.is_authenticated or user not in members:
            await self.close()
            return

        # присоединяемся к группе
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message', '').strip()
        user = self.scope['user']

        if message and user.is_authenticated:
            # сохраняем сообщение в беседе
            msg = await self.save_message(user, message)

            # отправляем всем участникам в группе
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "chat_message",
                    "message": msg.content,
                    "username": user.username,
                    "timestamp": msg.timestamp.isoformat(),
                }
            )

    async def chat_message(self, event):
        # пересылаем данные клиенту
        await self.send(text_data=json.dumps({
            "message": event['message'],
            "username": event['username'],
            "timestamp": event['timestamp'],
        }))

    @database_sync_to_async
    def save_message(self, user, content):
        convo = Conversation.objects.get(id=self.convo_id)
        return Message.objects.create(conversation=convo, author=user, content=content)
