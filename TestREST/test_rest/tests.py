from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

from .models import TestRESTModel


class UniversalTest(APITestCase):

    def setUp(self):
        user1 = User.objects.create(username='admin', email='admin@gmail.com', password='password')
        user2 = User.objects.create(username='admin2', email='admin2@gmail.com', password='password')

        TestRESTModel.objects.create(title='Title 1', content='Content 1', age=19, author=user1)
        TestRESTModel.objects.create(title='Title 2', content='Content 2', age=20, author=user2)
        TestRESTModel.objects.create(title='Title 3', content='Content 3', age=21, author=user1)
        print('SetUp-------------')

    def test_update_patch(self):
        response = self.client.patch('/test-rest/universal/8/', {#'title': 'Fuck',
                                                              'content': 'Fucking content',
                                                              #'age': 24,
                                                              'author': 2}, format='json')
        print('update_patch')
        print('status: ', response.status_code)
        print('data: ', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_list(self):
        response = self.client.get('/test-rest/universal/')
        print('list_get')
        print('status: ', response.status_code)
        print('data: ', response.data)
