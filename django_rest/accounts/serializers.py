from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    email = serializers.CharField(style={'input_type': 'email'})

    def create(self, validated_data):
        if validated_data['password'] != validated_data['password2']:
            raise serializers.ValidationError({'password': 'Passwords doesn\'t match'})

        validated_data['password'] = make_password(validated_data['password'])

        validated_data.pop('password2', None)
        return super().create(validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    def post(self):
        pass
