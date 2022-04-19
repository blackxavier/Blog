from rest_framework import generics, permissions, status, viewsets
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from blog_api.permissions import AuthorAllStaffAllButEditOrReadOnly
from blog_api.serializers import (
    CategoryModelSerializer,
    PostDetailSerializer,
    PostsReadSerializer,
    PostWriteModelSerializer,
    PublishPostSerializer,
    ReadCommentModelSerializer,
    WriteCommentSerializer,
)
from blog_app.models import CategoryModel, CommentModel, PostModel


class PostListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = PostModel.publishedpost.all()
    serializer_class = PostsReadSerializer


class PostRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PostModel.publishedpost.all()

    serializer_class = PostDetailSerializer
    lookup_field = "slug"

    def get_permissions(self):
        author_request = ["POST", "PUT", "PATCH", "DELETE"]
        if self.request.method in author_request:
            permission_classes = [AuthorAllStaffAllButEditOrReadOnly, IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        get_methods = ["GET", "HEAD", "OPTIONS"]
        if self.request.method in get_methods:
            return PostDetailSerializer
        return PostWriteModelSerializer


class PostCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = PostModel.objects.all()
    serializer_class = PostWriteModelSerializer

    def perform_create(self, serializer):

        return serializer.save(author=self.request.user)


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
    # create comment
    permission_classes = [IsAuthenticated]
    queryset = CommentModel.objects.all()

    def get_serializer_class(self):
        method_list = ["POST", "PUT", "DELETE", "PATCH"]
        if self.request.method in method_list:
            return WriteCommentSerializer

        return ReadCommentModelSerializer

    def perform_create(self, serializer):
        serializer.save(post_id=self.request.id)


class PublishPostView(generics.UpdateAPIView):
    # change status=publish
    permission_classes = [AuthorAllStaffAllButEditOrReadOnly]
    serializer_class = PublishPostSerializer
    queryset = PostModel.objects.all()
    lookup_field = "slug"


class AllPostDrafts(generics.ListAPIView):
    # All drafts by user
    
    serializer_class = PostsReadSerializer
    permissions_classes = [AuthorAllStaffAllButEditOrReadOnly, IsAuthenticated]

    def get_queryset(self):
        draftedpost = PostModel.draftedpost.filter(author=self.request.user)
        return draftedpost
