from django.urls import path
from django.urls.resolvers import URLPattern
from  . import blogviews
from blog.api.views import post_list

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views

urlpatterns = [
    path('',blogviews.post_list,name='post_list'),
    path('post/<int:pk>/', blogviews.post_detail, name='post_detail'),
    path('post/new/', blogviews.post_new, name='post_new'),
    path('post/<int:pk>/edit/', blogviews.post_edit, name='post_edit'),
    path('drafts/', blogviews.post_draft_list, name='post_draft_list'),
    path('post/<pk>/publish/', blogviews.post_publish, name='post_publish'),
    path('post/<pk>/remove/', blogviews.post_remove, name='post_remove'),
    path('post/<int:pk>/comment/', blogviews.add_comment_to_post, name='add_comment_to_post'),
    path('comment/<int:pk>/approve/', blogviews.comment_approve, name='comment_approve'),
    path('comment/<int:pk>/remove/', blogviews.comment_remove, name='comment_remove'),

    #api
    path('api/token/', views.obtain_auth_token),
    path('api/post/', post_list.posts.as_view()),
    path('api/draft/', post_list.drafts.as_view()),
    path('api/post/<int:pk>/', post_list.post_detail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)