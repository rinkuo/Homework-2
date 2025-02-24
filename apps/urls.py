from django.urls import path
from .views import (
    PostListCreateView, PostDetailView, CommentListCreateView,
    TagListView, TagListAPIView, CategoryListAPIView, CategoryPostListAPIView,
)

urlpatterns = [
    path('posts/', PostListCreateView.as_view(), name='post-list'),
    path('posts/<slug:post_slug>/', PostDetailView.as_view(), name='post-detail'),
    path("posts/<slug:post_slug>/comments/", CommentListCreateView.as_view(), name="post-comments"),
    path('categories/', CategoryListAPIView.as_view(), name='category-list'),
    path('categories/<slug:category_slug>/posts/', CategoryPostListAPIView.as_view(), name='category-posts'),
    path('tags/', TagListAPIView.as_view(), name='tag-list'),
    path("tags/<slug:tag_slug>/posts/", TagListView.as_view(), name="tag-posts"),
]
