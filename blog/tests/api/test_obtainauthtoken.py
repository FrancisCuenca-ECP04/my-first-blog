from django.test import TestCase

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.test import APIRequestFactory
from rest_framework.response import Response

class TestObtainAuthToken(TestCase):
    """ Create new user, generate token, check if user token == response token """

    def test_checkToken(self):
        user = User.objects.create_user('testkokong','testkokong@email.com','testkokong')
        token, created = Token.objects.get_or_create(user=user)

        data = {"username":"testkokong","password":"testkokong"}

        self.view = ObtainAuthToken.as_view()
        self.request_factory = APIRequestFactory()
        request = self.request_factory.post('/api/token/', data)
        response = self.view(request)

        self.assertEqual(token.key, response.data['token'])
        self.assertNotEqual('random_text', response.data['token'])
    
    def test_checkToken_wrong_credentials(self):
        user = User.objects.create_user('testkokong','testkokong@email.com','testkokong')
        token, created = Token.objects.get_or_create(user=user)

        data = {"username":"testkokong177","password":"testkokong013"}

        self.view = ObtainAuthToken.as_view()
        self.request_factory = APIRequestFactory()
        request = self.request_factory.post('/api/token/', data)
        response = self.view(request)

        self.assertEqual(response.data['non_field_errors'][0], 'Unable to log in with provided credentials.')
        
        