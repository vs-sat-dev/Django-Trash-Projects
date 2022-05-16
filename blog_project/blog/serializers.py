from rest_framework import serializers

from .models import Post
from .validators import LessThanValidator, GreaterThanValidator


class PostSerializer(serializers.ModelSerializer):
    title = serializers.CharField(validators=[LessThanValidator(3), GreaterThanValidator(128)])
    body = serializers.CharField(validators=[LessThanValidator(3), GreaterThanValidator(4096)])
    author = serializers.ReadOnlyField(source='author.username')
    
    class Meta:
        model = Post
        fields = ['title', 'body', 'author']
        
class PostCreateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(validators=[LessThanValidator(3), GreaterThanValidator(128)])
    body = serializers.CharField(validators=[LessThanValidator(3), GreaterThanValidator(4096)])
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = Post
        fields = ['title', 'body', 'author']
    
    


