import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.utils.timezone import now
from channels.layers import get_channel_layer

from .models import Room, Message, Visit


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        
        print('Room Name: ', self.room_name)

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
        type = text_data_json['type']
        user = self.scope['user']
        room_name = self.scope['url_route']['kwargs']['room_name']
        if type == 'message':
            message = text_data_json['message']
            
            try:
                room = Room.objects.get(roomname=room_name)
                
                msg = Message.objects.create(room=room, message=message, user=user)
                
                print('Got message ', message, ' user ', user, ' room ', Room, ' msg ', msg)

                # Send message to room group
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message
                    }
                )
                
                
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(room_name + '_notification',
                                                        {'message': message,
                                                         'type': 'notification_message',})
                
                
            except:
                print('Room was not found')
            
        elif type == 'read':
            room_name = self.scope['url_route']['kwargs']['room_name']
            print('room_name ', room_name)
            try:
                room = Room.objects.get(roomname=room_name)
                try:
                    visit = Visit.objects.filter(user=user, room=room).first()
                    visit.last_visit = now()
                except:
                    visit = Visit.objects.create(user=user, room=room, last_visit=now())
                #print('type', type, ' user ', user)
                #print('Visit user: ', visit.user, ' room ', visit.room, ' last_visit ', visit.last_visit)
            except:
                print('Room was not found')

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))


class RoomNotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = self.room_name
        
        print('Room Name: ', self.room_name)

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    
    def receive(self, text_data):
        async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'notification_message',
                        'message': message
                    }
                )
    
    # Receive message from room group
    def notification_message(self, event):
        message = event['message']
        room_name = self.scope['url_route']['kwargs']['room_name'][:-13]
        user = self.scope['user']
        
        print('Notification: ', message, ' room ', room_name)
        try:
            room = Room.objects.get(roomname=room_name)
            
            print('Notification user ', user, ' room ', Room)
            
            try:
                visit = Visit.objects.filter(user=user, room=room).first()
                messages = Message.objects.filter(room=room, created__lt=visit.last_visit)
                print('Notification message: ', messages)
                # Send message to WebSocket
                self.send(text_data=json.dumps({
                    'message': message
                }))
            except:
                print('Visit was not found')

        except Exception as e:
            print('Room was not found in notifications. ', e)
