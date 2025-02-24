from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Post, Comment, Category, Tag
from .serializers import (
    PostSerializer, PostCreateSerializer, CommentSerializer, RecursiveCommentSerializer,
    CategorySerializer, TagSerializer
)


class PostListCreateView(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailView(APIView):
    def get(self, request, id):
        post = get_object_or_404(Post, id=id)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, id):
        post = get_object_or_404(Post, id=id)
        serializer = PostCreateSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        post = get_object_or_404(Post, id=id)
        post.delete()
        return Response({"message": "Post deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class CommentListCreateView(APIView):
    def get(self, request, post_slug):
        """Fetch comments for a specific post"""
        post = get_object_or_404(Post, slug=post_slug)
        comments = Comment.objects.filter(post=post, parent_comment__isnull=True)  # Faqat root commentlar
        all_comments_count = Comment.objects.filter(post=post).count()  # Hamma commentlarni hisoblash

        serializer = CommentSerializer(comments, many=True)
        return Response({"count": all_comments_count, "next": None, "previous": None, "results": serializer.data})

    def post(self, request, post_slug):
        post = get_object_or_404(Post, slug=post_slug)
        data = request.data.copy()
        data["post"] = post.id  # Post ID ni qo‘shamiz

        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()  # Post ID bo‘lishi shart
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)

class CategoryListView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class CategoryPostListView(APIView):
    def get(self, request, category_id):
        posts = Post.objects.filter(category_id=category_id)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class TagListView(APIView):
    def get(self, request):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)


class TagPostListView(APIView):
    def get(self, request, tag_id):
        posts = Post.objects.filter(tags__id=tag_id)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
