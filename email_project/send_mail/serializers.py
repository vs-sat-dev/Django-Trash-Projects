from rest_framework import serializers
from django.core.mail import EmailMessage
from time import sleep

from .tasks import send_mail


class EmailSendSerializer(serializers.Serializer):
    email = serializers.EmailField()
    body = serializers.CharField()

    def create(self, validated_data):
        result = send_mail.delay(validated_data['email'], validated_data['body'])
        print('Task_Result ', result)

        """mail_subject = 'Your text from test django project'
        email = EmailMessage(mail_subject, validated_data['body'], to=[validated_data['email']])
        email.send()"""

        return validated_data
