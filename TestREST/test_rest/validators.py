from rest_framework.serializers import ValidationError


class LessThanValidator:
    def __init__(self, base):
        self.base = base

    def __call__(self, value):
        if value < self.base:
            raise ValidationError({'error': f'Age must be greater or equal {self.base}'})
