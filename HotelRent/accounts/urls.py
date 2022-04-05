from django.urls import path

from . import views


app_name = 'accounts'

urlpatterns = [
    path('register', views.register, name='register'),
    path('email-activation/<uidb64>/<token>/', views.email_activation, name='email-activation'),
    path('login', views.login_user, name='login'),
    path('profile/<str:username>', views.profile, name='profile'),
    path('logout', views.logout_user, name='logout'),
    path('image-change', views.image_change, name='image-change'),
    path('email-change', views.email_change, name='email-change'),
    path('password-change', views.password_change, name='password-change'),
]
