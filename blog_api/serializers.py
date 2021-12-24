from blog_app.models import CommentModel, PostModel, CategoryModel
from rest_framework import serializers
from users.models import User
from taggit.serializers import TagListSerializerField, TaggitSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name")


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


class WritePostModelSerializer(TaggitSerializer, serializers.ModelSerializer):
    pass


class PostModelSerializer(TaggitSerializer, serializers.ModelSerializer):
    category = CategoryModelSerializer()
    author = UserSerializer()
    tags = TagListSerializerField()

    class Meta:
        model = PostModel
        fields = [
            "id",
            "title",
            "excerpt",
            "content",
            "slug",
            "published_date",
            "author",
            "category",
            "status",
            "tags",
        ]


class ReadCommentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentModel
        fields = ["id", "comment_text", "date_created"]


class WriteCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentModel
        fields = ["comment_text"]
