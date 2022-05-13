from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import PostViewSet

router = DefaultRouter()
router.register('post', PostViewSet)


urlpatterns = [
]

urlpatterns += router.urls
