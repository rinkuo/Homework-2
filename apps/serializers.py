from rest_framework import serializers
from django.utils.text import slugify
from rest_framework.generics import get_object_or_404
from .models import Author, Category, Tag, Post, Comment


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'email', 'bio']

    def validate_email(self, value):
        if "@" not in value or "." not in value:
            raise serializers.ValidationError("Noto‘g‘ri email formati!")
        return value


class CategorySerializer(serializers.ModelSerializer):
    posts_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'posts_count']

    def get_posts_count(self, obj):
        return obj.post_set.count()


class TagSerializer(serializers.ModelSerializer):
    posts_count = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'posts_count']

    def get_posts_count(self, obj):
        return obj.post_set.count()


class RecursiveCommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author_name', 'author_email', 'content', 'created_at', 'parent_comment', 'replies']

    def get_replies(self, obj):
        if obj.level < 3:
            children = obj.children.all()
            return RecursiveCommentSerializer(children, many=True).data
        return []

    def create(self, validated_data):
        request = self.context.get('request')
        post_slug = request.parser_context['kwargs'].get('post_slug')
        post = get_object_or_404(Post, slug=post_slug)
        validated_data["post"] = post
        return super().create(validated_data)

class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author_name', 'author_email', 'content', 'created_at', 'parent_comment', 'replies']

    def get_replies(self, obj):
        replies = Comment.objects.filter(parent_comment=obj)
        return CommentSerializer(replies, many=True).data


class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    category = CategorySerializer()
    tags = TagSerializer(many=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'content', 'author', 'category',
            'tags', 'created_at', 'updated_at', 'status', 'comments_count'
        ]

    def get_comments_count(self, obj):
        return obj.comments.count()

class PostCreateSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    category = CategorySerializer()
    tags = TagSerializer(many=True)
    slug = serializers.CharField(read_only=True)

    class Meta:
        model = Post
        fields = ['title', 'content', 'author', 'category', 'tags', 'status', 'slug']

    def create(self, validated_data):
        author_data = validated_data.pop('author')
        category_data = validated_data.pop('category')
        tags_data = validated_data.pop('tags')

        author, _ = Author.objects.get_or_create(email=author_data['email'], defaults=author_data)
        category, _ = Category.objects.get_or_create(name=category_data['name'], defaults=category_data)

        validated_data['slug'] = slugify(validated_data['title'])
        post = Post.objects.create(author=author, category=category, **validated_data)

        for tag_data in tags_data:
            tag, _ = Tag.objects.get_or_create(name=tag_data['name'], defaults=tag_data)
            post.tags.add(tag)

        return post
