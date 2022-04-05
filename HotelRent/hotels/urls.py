from django.urls import path

from . import views


app_name = 'hotels'

urlpatterns = [
    path('hotels', views.hotels, name='hotels'),
]
