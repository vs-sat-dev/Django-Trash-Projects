from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from .models import Post


class PostTest(APITestCase):
    def setUp(self):
        password = make_password('password')
        self.user1 = User.objects.create(username='User1', email='user1@gmail.com', password=password)
        self.user2 = User.objects.create(username='User2', email='user2@gmail.com', password=password)
        self.user3 = User.objects.create(username='User3', email='user3@gmail.com', password=password)
        
        token_response = self.client.post('http://127.0.0.1:8000/accounts/api/token/', {'username': 'User1',
                                                                             'password': 'password'}, 
                               format='json')
        self.access_token = token_response.data['access']
        self.refresh_token = token_response.data['refresh']
        
        print('CHECKS---------------------------------------------')
        print(self.access_token)
        
        Post.objects.create(title='title1', body='body1', author=self.user1)
        Post.objects.create(title='title2', body='body2', author=self.user2)
        Post.objects.create(title='title3', body='body3', author=self.user3)
    
    def test_get_list(self):
        response = self.client.get('http://127.0.0.1:8000/blog/post/')
        #self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_update(self):
        response = self.client.put('http://127.0.0.1:8000/blog/post/1/', {'title': 'Changed title',
                                                              'body': 'Changed body'}, format='json')
        #self.assertEqual(response.status_code, status.HTTP_200_OK)
