from celery import shared_task
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.core.mail import send_mail

from time import sleep
from email_project.celery import app


@shared_task
def send_mail(email, body):
    sleep(15)
    mail_subject = 'Your text from test django project'
    email = EmailMessage(mail_subject, body, to=[email])
    email.send()
    """with open('file.txt', 'w') as file:
        file.write('LogStart')
        #sleep(10)
        file.write('LogEnd')"""

    return None
