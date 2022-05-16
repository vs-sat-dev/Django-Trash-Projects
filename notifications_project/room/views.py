from django.shortcuts import render
from django.views.generic import ListView
from rest_framework import viewsets, generics, mixins
from rest_framework import permissions
import json

from .models import Room, Message, Visit
from .serializers import RoomSerializer, MessageSerializer
from .permissions import IsOwnerOrReadOnly, ActionBasedPermission


class RoomViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        permissions.IsAuthenticated: ['create'],
        IsOwnerOrReadOnly: ['destroy', 'partial_update'],
        permissions.AllowAny: ['retrieve', 'list'] #Temporary permission
    }
    
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class MessageViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        permissions.IsAuthenticated: ['create'],#Temporaru permission
        IsOwnerOrReadOnly: ['destroy', 'partial_update'],
        permissions.AllowAny: ['retrieve', 'list'] #Temporary permission
    }
    
    def perform_create(self, serializer):
        
        """room = serializer.validated_data['room']
        try:
            visit = Visit.objects.get(user=self.request.user, room=room)
            visit.last_visit = now()
        except:
            visit = Visit.objects.create(user=self.request.user, room=room, last_visit=now())"""
        #print('Visit user: ', visit.user, ' room ', visit.room, ' last_visit ', visit.last_visit)
        
        serializer.save(user=self.request.user)


class RoomListView(ListView):
    template_name = 'rooms.html'
    model = Room
 

def room(request, room_name):
    return render(request, 'chat.html', {'room_name': room_name})
