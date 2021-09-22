from blog.models import Comment
from blog.serializers import CommentSerializer
from rest_framework import generics


class comment_list(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class post_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
