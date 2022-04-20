from django.db import transaction
from django.template.defaultfilters import slugify
from rest_framework import serializers
from taggit.serializers import TaggitSerializer, TagListSerializerField

from blog_app.models import CategoryModel, CommentModel, PostModel, blog_options
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "username", "first_name", "last_name")


class ReadCommentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentModel
        fields = ["id", "comment_text", "date_created"]


class CategoryModelSerializer(serializers.Serializer):
    category_name = serializers.CharField(max_length=200)

    def create(self, validated_data):
        return CategoryModel.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.category_name = validated_data.get(
            "category_name", instance.category_name
        )

        instance.save()
        return instance


class PostWriteModelSerializer(TaggitSerializer, serializers.ModelSerializer):
    class Meta:
        model = PostModel
        fields = ["title", "excerpt", "content", "status"]


class PostsReadSerializer(serializers.ModelSerializer):

    author = UserSerializer()

    class Meta:
        model = PostModel
        fields = ["title", "excerpt", "slug", "author", "published_date"]


class CommentInPostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentModel
        fields = ["comment_text", "date_created"]


class PostDetailSerializer(TaggitSerializer, serializers.ModelSerializer):
    category = serializers.SlugRelatedField(read_only=True, slug_field="category_name")
    comments = CommentInPostDetailSerializer(many=True)
    author = serializers.SlugRelatedField(read_only=True, slug_field="email")

    tags = TagListSerializerField()

    class Meta:
        model = PostModel
        fields = [
            "title",
            "excerpt",
            "slug",
            "author",
            "published_date",
            "content",
            "status",
            "category",
            "tags",
            "comments",
        ]


class ReadCommentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentModel
        fields = ["id", "comment_text", "date_created"]


class WriteCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentModel
        fields = ["comment_text"]


class StatusChangePostSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=blog_options, default="draft")

    def update(self, instance, validated_data):

        instance.status = validated_data.get("status", instance.status)

        instance.save(update_fields=["status"])
        return instance


class TagListSerializer(TaggitSerializer):
    tags = TagListSerializerField()
