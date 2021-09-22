from django.urls import path
from django.urls.resolvers import URLPattern
from  . import views
from blog.api.views import post

from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('',views.post_list,name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('drafts/', views.post_draft_list, name='post_draft_list'),
    path('post/<pk>/publish/', views.post_publish, name='post_publish'),
    path('post/<pk>/remove/', views.post_remove, name='post_remove'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),

    #api
    path('api/post/', post.post_list.as_view()),
    path('api/post/<int:pk>/', post.post_detail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)