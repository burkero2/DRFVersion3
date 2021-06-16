from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Post

# Create your tests here.
class PostListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='a', password='pass')

    def test_can_list_posts(self):
        a = User.objects.get(username='a')
        Post.objects.create(owner=a, title='a title')
        
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data, len(response.data))

    def test_anon_cant_create_post(self):
        response = self.client.post('/posts/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_create_post(self):
        self.client.login(username='a', password='pass')
        response = self.client.post('/posts/', {'title': 'a title'})
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_cant_update_somebodys_post(self):
        self.client.login(username='a', password='pass')
        response = self.client.put('/posts/2/', {'title': 'yay'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)