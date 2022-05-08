from django.urls import path
#from rest_framework_simplejwt.views import
from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework.test import APITestCase

from .views import TestRESTView, TestRESTUpdateView, UniversalView


router = SimpleRouter()
router.register('universal', UniversalView)

app_name = 'test-rest'

urlpatterns = [
    path('list/', TestRESTView.as_view()),
    #path('list/<int:pk>/', TestRESTView.as_view()),
    path('list/<int:pk>/', TestRESTUpdateView.as_view()),
    #path('universal/', UniversalView.as_view({'get': 'list'})),
    #path('universal/<int:pk>/', UniversalView.as_view({'put': 'update'})),
    #path('universal/detail/<int:pk>/', UniversalView.as_view({'get': 'retrieve'})),
]

urlpatterns += router.urls
