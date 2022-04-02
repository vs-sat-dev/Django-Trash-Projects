from django.urls import path

from . import views


urlpatterns = [
    path('register', views.register, name='register'),
    #path(r'email-activation/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
    path('email-activation/<uidb64>/<token>/', views.email_activation, name='email-activation')
]
