from django.test import TestCase 
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from rest_framework.response import Response
from blog.api.views import comment,post_list
from rest_framework.authtoken.models import Token
from rest_framework.test import force_authenticate

class TestPostList(TestCase):
    """Tests GET and POST methods of comment"""

    def setUp(self):
        self.user = User.objects.create_user('testkokong','testkokong@email.com','testkokong')
        token, created = Token.objects.get_or_create(user=self.user)
        self.request_factory = APIRequestFactory()

        #create new post
        data = {"author":self.user.id, "title":"test_post", "text":"testkokong"}

        self.view = post_list.posts.as_view()
        request = self.request_factory.post('/api/post/', data)
        force_authenticate(request, user=self.user)
        response = self.view(request)

        self.post_id = response.data['id']

        #create new comment
        data = {"author":self.user.id, "post": self.post_id, "text":"This is a test comment."}

        self.view = comment.comments.as_view()
        request = self.request_factory.post('/api/comment/', data)
        force_authenticate(request, user=self.user)
        response = self.view(request)

        #create 2nd comment
        data = {"author":self.user.id, "post": self.post_id, "text":"This is the 2nd comment."}

        self.view = comment.comments.as_view()
        request = self.request_factory.post('/api/comment/', data)
        force_authenticate(request, user=self.user)
        response = self.view(request)

    def test_comment_list(self):
        """Testing GET method of comment"""

        self.view = comment.comments.as_view() 
        request = self.request_factory.get('/api/post/' + str(self.post_id) + '/comments')
        force_authenticate(request, user=self.user)
        response = self.view(request, pk = self.post_id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['post'], self.post_id)
        self.assertEqual(response.data[0]['text'],'This is a test comment.')
        self.assertEqual(response.data[1]['post'], self.post_id)
        self.assertEqual(response.data[1]['text'],'This is the 2nd comment.')
    
    def test_comment_list_nonexistent(self):
        """Testing GET method of comment"""

        self.view = comment.comments.as_view() 
        request = self.request_factory.get('/api/post/1/comments')
        force_authenticate(request, user=self.user)
        response = self.view(request, pk = 1)

        self.assertEqual(response.status_code, 404)

    def test_comment_delete(self):
        """Testing DELETE method of comment"""

        self.view = comment.comment_detail.as_view() 
        request = self.request_factory.delete('/api/comment/detail/' + str(1) + '/')
        force_authenticate(request, user=self.user)
        response = self.view(request, pk = 1)

        self.assertEqual(response.status_code, 204)

    def test_comment_delete_nonexistent(self):
        """Testing DELETE method of comment"""

        self.view = comment.comment_detail.as_view() 
        request = self.request_factory.delete('/api/comment/detail/' + str(177013) + '/')
        force_authenticate(request, user=self.user)
        response = self.view(request, pk = 177013)

        self.assertEqual(response.status_code, 404)
