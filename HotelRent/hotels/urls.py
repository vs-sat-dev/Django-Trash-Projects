from django.urls import path

from . import views


app_name = 'hotels'

urlpatterns = [
    path('hotels', views.hotels, name='hotels'),
    path('hotel-detail/<str:city>/<str:category>/<slug:slug>', views.hotel_detail, name='hotel-detail'),
    path('create-hotel', views.create_hotel, name='create-hotel'),
]
