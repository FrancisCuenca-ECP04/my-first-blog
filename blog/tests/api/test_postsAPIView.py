from django.test import TestCase 
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from rest_framework.response import Response
from blog.api.views import post_list
from rest_framework.authtoken.models import Token
from rest_framework.test import force_authenticate

class TestPostList(TestCase):
    """Tests GET and POST methods of post_list view and GET, PUT, DELETE of post_detail"""

    def setUp(self):
        
        #create user
        self.user = User.objects.create_user('testkokong','testkokong@email.com','testkokong')
        token, created = Token.objects.get_or_create(user=self.user)
        
        #create 2nd User
        self.user_wrong = User.objects.create_user('testkokong2','testkokong2@email.com','testkokong')
        token, created = Token.objects.get_or_create(user=self.user_wrong)

        self.request_factory = APIRequestFactory()
  
        #creating post in database
        data = {"author":self.user.id, "title":"test_post", "text":"testkokong"}

        self.view = post_list.posts.as_view()
        request = self.request_factory.post('/api/post/', data)
        force_authenticate(request, user=self.user)
        response = self.view(request)

        self.post_id = response.data['id']
    
    def test_posts_list(self):   
        """Testing GET method of post_list"""

        self.view = post_list.posts.as_view() 
        request = self.request_factory.get('/api/post/')
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, 200)

    def test_post_create(self):
        """Testing POST method of post_list"""

        data = {"author":self.user.id, "title":"test_post", "text":"testkokong"}

        self.view = post_list.posts.as_view()
        request = self.request_factory.post('/api/post/', data)
        force_authenticate(request, user=self.user)
        response = self.view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['author'], self.user.id)
        self.assertEqual(response.data['title'], 'test_post')
        self.assertEqual(response.data['text'], 'testkokong')
        
    def test_post_detail(self):
        """Testing GET method of post_detail"""
        post_id = self.post_id

        #get post details
        self.view = post_list.post_detail.as_view()
        request = self.request_factory.get('/api/post/' + str(post_id) + '/')
        force_authenticate(request, user=self.user)
        response = self.view(request,pk=post_id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['author'], self.user.id)
        self.assertEqual(response.data['title'], 'test_post')
        self.assertEqual(response.data['text'], 'testkokong')
    
    def test_post_detail_nonexisting_post(self):
        """Testing GET method of post_detail with nonexisting post"""

        #get post details
        self.view = post_list.post_detail.as_view()
        request = self.request_factory.get('/api/post/177013/')
        force_authenticate(request, user=self.user)
        response = self.view(request,pk=177013)

        self.assertEqual(response.status_code, 404)

    def test_post_edit(self):
        """Testing PUT method of post_detail"""

        post_id = self.post_id

        #edit post details
        newdata = {"author":self.user.id, "title":"edit_post", "text":"testkokong!"}

        self.view = post_list.post_detail.as_view()
        request = self.request_factory.put('/api/post/' + str(post_id) + '/', newdata)
        force_authenticate(request, user=self.user)
        response = self.view(request,pk=post_id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['author'], self.user.id)
        self.assertEqual(response.data['title'], newdata['title'])
        self.assertEqual(response.data['text'], newdata['text'])

    def test_post_edit_wrong_user(self):

        post_id = self.post_id

        #edit post details
        newdata = {"author":self.user.id, "title":"edit_post", "text":"testkokong!"}

        self.view = post_list.post_detail.as_view()
        request = self.request_factory.put('/api/post/' + str(post_id) + '/', newdata)
        force_authenticate(request, user=self.user_wrong)
        response = self.view(request,pk=post_id)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['message'],'You are not authorized to edit this post.')

    def test_post_delete(self):
        """Test DELETE method of post_detail"""

        post_id = self.post_id

        #get post details
        self.view = post_list.post_detail.as_view()
        request = self.request_factory.delete('/api/post/' + str(post_id) + '/')
        force_authenticate(request, user=self.user)
        response = self.view(request,pk=post_id)

        self.assertEqual(response.status_code, 204)

    def test_post_delete_wrong_user(self):

        post_id = self.post_id

        #delete post details
        newdata = {"author":self.user.id, "title":"edit_post", "text":"testkokong!"}

        self.view = post_list.post_detail.as_view()
        request = self.request_factory.delete('/api/post/' + str(post_id) + '/', newdata)
        force_authenticate(request, user=self.user_wrong)
        response = self.view(request,pk=post_id)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['message'],'You are not authorized to delete this post.')
    
    def test_post_delete_nonexistent(self):
        """Test DELETE method of post_detail"""

        #get post details
        self.view = post_list.post_detail.as_view()
        request = self.request_factory.delete('/api/post/177013/')
        force_authenticate(request, user=self.user)
        response = self.view(request,pk=177013)

        self.assertEqual(response.status_code, 404)
