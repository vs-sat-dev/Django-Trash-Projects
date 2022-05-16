from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import PostViewSet, PostCreateView

router = DefaultRouter()
router.register('post', PostViewSet)


urlpatterns = [
    path('post/create/', PostCreateView.as_view())
]

urlpatterns += router.urls
