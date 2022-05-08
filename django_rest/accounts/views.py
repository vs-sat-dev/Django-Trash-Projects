from rest_framework import generics, views, permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth.models import User
from rest_framework.response import Response

from .serializers import RegisterSerializer
from .permissions import IsNotAuthenticated


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [IsNotAuthenticated]


class LogoutView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self):
        token = TokenRefreshView(token=self.request.data.get('refresh_token'))
        token.blacklist()
        return Response('You are logout.')
