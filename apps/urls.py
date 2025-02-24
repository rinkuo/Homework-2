from django.urls import path
from .views import (
    PostListCreateView, PostDetailView, CommentListCreateView,
    CategoryListView, TagListView
)

urlpatterns = [
    path('posts/', PostListCreateView.as_view(), name='post-list'),
    path('posts/<int:id>/', PostDetailView.as_view(), name='post-detail'),
    path("posts/<slug:post_slug>/comments/", CommentListCreateView.as_view(), name="post-comments"),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('tags/', TagListView.as_view(), name='tag-list'),
]
