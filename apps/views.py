from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Post, Comment, Category, Tag
from .serializers import (
    PostSerializer, PostCreateSerializer, CommentSerializer, TagSerializer, CategorySerializer,
)
#getda 3 xil logika ishlatilgan Post,Comment, Tag

class PostListCreateView(APIView):
    def get(self, request):
        queryset = Post.objects.filter(status="published").order_by('-created_at')

        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_queryset = paginator.paginate_queryset(queryset, request)

        serializer = PostSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailView(APIView):
    def get(self, request, post_slug):
        post = get_object_or_404(Post, slug=post_slug)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, post_slug):
        post = get_object_or_404(Post, slug=post_slug)
        serializer = PostCreateSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_slug):
        post = get_object_or_404(Post, slug=post_slug)
        post.delete()
        return Response({"message": "Post deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class CommentListCreateView(APIView):
    def get(self, request, post_slug):
        post = get_object_or_404(Post, slug=post_slug)
        comments = Comment.objects.filter(post=post, parent_comment__isnull=True)
        all_comments_count = Comment.objects.filter(post=post).count()

        serializer = CommentSerializer(comments, many=True)
        return Response({"count": all_comments_count, "next": None, "previous": None, "results": serializer.data})

    def post(self, request, post_slug):
        post = get_object_or_404(Post, slug=post_slug)
        data = request.data.copy()
        data["post"] = post.id

        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save(post=post)
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)

class CategoryListAPIView(APIView):
    def get(self, request):
        queryset = Category.objects.all()

        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_queryset = paginator.paginate_queryset(queryset, request)

        serializer = CategorySerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

class CategoryPostListAPIView(APIView):
    def get(self, request, category_slug):
        category = get_object_or_404(Category, slug=category_slug)

        queryset = Post.objects.filter(category=category, status="published").order_by('-created_at')

        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_queryset = paginator.paginate_queryset(queryset, request)

        serializer = PostSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

class TagListAPIView(APIView):
    def get(self, request):
        queryset = Tag.objects.all()

        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_queryset = paginator.paginate_queryset(queryset, request)

        serializer = TagSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

class TagListView(APIView):
    def get(self, request, tag_slug):
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = Post.objects.filter(tags=tag)
        serializer = PostSerializer(posts, many=True)

        response_data = {
            "count": posts.count(),
            "next": None,
            "previous": None,
            "results": serializer.data
        }

        return Response(response_data)
