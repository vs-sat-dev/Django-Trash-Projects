from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, UpdateAPIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, UpdateModelMixin, RetrieveModelMixin
from django.http import JsonResponse
from time import sleep

from .serializers import TestRESTSerializer
from .models import TestRESTModel
from .tasks import sleepy


class UniversalView(ListModelMixin, UpdateModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = TestRESTModel.objects.all()
    serializer_class = TestRESTSerializer
    throttle_scope = 'univer'

    def get(self, request, *args, **kwargs):
        print('Celery Checks1')
        # sleepy(10)
        print('Celery Checks2')
        return self.list(request, *args, **kwargs)

    """def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)"""


class TestRESTView(ListCreateAPIView):
    queryset = TestRESTModel.objects.all()
    serializer_class = TestRESTSerializer

    def get(self, *args, **kwargs):
        print('Fuck!')
        sleepy.delay((10,))
        print('Fuck End!')
        return JsonResponse([
            {
                'one': 'element',
                'two': 'elements'
            },
            {
                'three': True,
                'four': False
            }
        ], safe=False)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class TestRESTUpdateView(UpdateAPIView):
    queryset = TestRESTModel.objects.all()
    serializer_class = TestRESTSerializer
