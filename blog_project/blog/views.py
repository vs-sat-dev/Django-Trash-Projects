from django.shortcuts import render
from rest_framework import mixins, generics, viewsets, permissions
from rest_framework.authentication import TokenAuthentication

from .models import Post
from .serializers import PostSerializer, PostCreateSerializer
from .permissions import ActionBasedPermission, AuthorAllStaffAllButEditOrReadOnly, IsOwnerOrReadOnly


class PostViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                 mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        #permissions.IsAuthenticated: ['create'],
        IsOwnerOrReadOnly: ['update', 'destroy', 'partial_update'],
        permissions.AllowAny: ['retrieve', 'list']
    }


class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes= [permissions.IsAuthenticated]
    
