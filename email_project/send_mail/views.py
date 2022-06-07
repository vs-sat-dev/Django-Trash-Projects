from django.shortcuts import render
from rest_framework import generics

from .serializers import EmailSendSerializer


class EmailSendView(generics.CreateAPIView):
    serializer_class = EmailSendSerializer
