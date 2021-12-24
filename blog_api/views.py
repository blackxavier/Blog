from rest_framework import permissions
from blog_app.models import CommentModel, PostModel, CategoryModel
from blog_api.serializers import (
    PostModelSerializer,
    CategoryModelSerializer,
    ReadCommentModelSerializer,
    WriteCommentSerializer,
)
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny


class PostListView(generics.ListAPIView):
    queryset = PostModel.publishedpost.all()
    serializer_class = PostModelSerializer


class CategoryViewset(viewsets.ModelViewSet):
    """
    The category viewset provides CRUD operations on the category model

    """

    serializer_class = CategoryModelSerializer
    queryset = CategoryModel.objects.all()

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class CommentCreateReadView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = CommentModel.objects.all()

    def get_serializer_class(self):
        method_list = ["POST", "PUT", "DELETE", "PATCH"]
        if self.request.method in method_list:
            return WriteCommentSerializer

        return ReadCommentModelSerializer

    def perform_create(self, serializer):
        serializer.save(post_id=self.request.id)

    # def get_serializer_class(self):
    #     if self.action in ("list", "retrieve"):
    #         return ReadCommentModelSerializer
    #     else:
    #         return WriteCommentSerializer
