import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from medcoapp.models import account
from chat.models import DirectMessage


class PersonalChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        current_user_id=int(self.scope['query_string'])
        other_user_id = self.scope["url_route"]["kwargs"]["id"]
        self.room_name = (
            f"{current_user_id}_{other_user_id}"
            if int(current_user_id) > int(other_user_id)
            else f"{other_user_id}_{current_user_id}"
        )
        self.room_group_name = f"chat_{self.room_name}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        await super().disconnect(close_code)
    
    async def receive(self, text_data=None, bytes_data=None):
        data=json.loads(text_data)
        print(data, 'djhfgfjdsahfgjhdsafg')
        message=data['message']
        # sender_username='nancy@gmail.com'
        # receiver_username='jancy@gmail.com'
        sender_username=data['senderUsername']
        receiver_username=data['receiverUsername']
        print('receiver name',receiver_username)
        print('sendername',sender_username)



        await self.save_message(
            sender_username=sender_username, receiver_username=receiver_username, message=message, thread_name=self.room_group_name
        )

        await self.channel_layer.group_send(
            self.room_group_name,

            {
                'type':"chat_message",
                'message':message,
                'senderUsername':sender_username,


            },

        )

    async def chat_message(self,event):
        print(event, 'dsffdddddddd')
        message=event['message']
        username=event['senderUsername']

        await self.send(
            text_data=json.dumps(
            {
                'message':message,
                'senderUsername':username,
                'messages':message,


            }
            )
        )

    @database_sync_to_async
    def get_messages(self):
        messages = []
        for instance in DirectMessage.objects.filter(thread_name=self.room_group_name):
            messages = DirectMessage(instance).data
        return messages

    @database_sync_to_async
    def save_message(self, sender_username,receiver_username, message, thread_name):
        sender_instance=account.objects.get(email=sender_username)
        reciever_instance=account.objects.get(email=receiver_username)
        print(sender_username,'sender_username')
        print(receiver_username,'receiver_username jj')
        DirectMessage.objects.create(sender=sender_instance, receiver=reciever_instance, message=message, thread_name=thread_name)