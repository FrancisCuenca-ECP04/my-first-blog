from blog.models import Post
from blog.serializers import PostSerializer
from rest_framework import generics

from django.utils import timezone

#todo - post_list should show published posts only - done!
#     - add authentication for post update and delete
#     - create unpublished view

class post_list(generics.ListCreateAPIView):
    ''' Published post list view '''
    queryset = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    serializer_class = PostSerializer

class post_draft_list(generics.ListCreateAPIView):
    ''' Unpublished post list view '''

class post_detail(generics.RetrieveUpdateDestroyAPIView):
    ''' Post detail view '''
    queryset = Post.objects.all()
    serializer_class = PostSerializer