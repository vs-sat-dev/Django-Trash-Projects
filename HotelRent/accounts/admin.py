from django.contrib import admin
from .models import Profile, EmailConfirmation


admin.site.register(Profile)
admin.site.register(EmailConfirmation)
