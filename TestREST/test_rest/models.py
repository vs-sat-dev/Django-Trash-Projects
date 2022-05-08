from django.db import models
from django.contrib.auth.models import User


class TestRESTModel(models.Model):
    title = models.CharField(max_length=128)
    content = models.TextField()
    age = models.IntegerField(default=18)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
