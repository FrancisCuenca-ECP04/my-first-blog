from blog.models import Post
from blog.serializers import PostSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.utils import timezone

class posts(APIView):
    """
    CRUD and List blog posts
    """  

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404

    #lists published posts
    def get(self, request):
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    #create posts
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)