from django.test import TestCase 
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from rest_framework.response import Response
from blog.api.views import post_list
from rest_framework.authtoken.models import Token
from rest_framework.test import force_authenticate

class TestPostList(TestCase):
    """Tests GET and POST methods of post_list views"""

    def test_posts_list(self):   
        user = User.objects.create_user('testkokong','testkokong@email.com','testkokong')
        token, created = Token.objects.get_or_create(user=user)
        self.view = post_list.posts.as_view()
        self.request_factory = APIRequestFactory()  
        request = self.request_factory.get('/api/post/')
        force_authenticate(request, user=user)
        response = self.view(request)
        self.assertEqual(response.status_code, 200)

    def test_post_create(self):
        user = User.objects.create_user('testkokong','testkokong@email.com','testkokong')
        token, created = Token.objects.get_or_create(user=user)

        data = {"author":user.id, "title":"test_post", "text":"testkokong"}

        self.view = post_list.posts.as_view()
        self.request_factory = APIRequestFactory()  
        request = self.request_factory.post('/api/post/', data)
        force_authenticate(request, user=user)
        response = self.view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['author'], user.id)
        self.assertEqual(response.data['title'], 'test_post')
        self.assertEqual(response.data['text'], 'testkokong')