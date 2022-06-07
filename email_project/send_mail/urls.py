from django.urls import path

from .views import EmailSendView

urlpatterns = [
    path('send_mail/', EmailSendView.as_view())
]
