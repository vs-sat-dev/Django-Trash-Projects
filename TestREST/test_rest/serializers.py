from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import TestRESTModel
from .validators import LessThanValidator


class TestRESTSerializer(ModelSerializer):
    #author = serializers.HiddenField()
    less_than_validator = LessThanValidator(16)
    age = serializers.IntegerField(validators=[less_than_validator])

    class Meta:
        model = TestRESTModel
        fields = '__all__'

    """def validate(self, data):
        if data['age'] < 18:
            raise serializers.ValidationError({'error': 'Age must be greater or equal 18'})
        return data"""
