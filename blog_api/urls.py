from django.urls import path
from rest_framework.routers import SimpleRouter

from blog_api.views import (AllPostDrafts, CategoryViewset,
                            CommentCreateReadView, PostCreateView,
                            PostListView, PostRetrieveView, PublishPostView)

app_name = "blog_api"


router = SimpleRouter()
router.register(r"categories", CategoryViewset, basename="category")
urlpatterns = [
    path("posts/", PostListView.as_view(), name="post_list"),
    path("users/me/drafted-posts/", AllPostDrafts.as_view(), name="post_drafted"),
    path("posts/<slug:slug>/", PostRetrieveView.as_view(), name="post_detail"),
    path("posts/<slug:slug>/publish/", PublishPostView.as_view(), name="post_publish"),
    path("posts/create/", PostCreateView.as_view(), name="post_create"),
    path(
        "posts/<int:pk>/comments/",
        CommentCreateReadView.as_view(),
        name="comment-list-create",
    ),
]
urlpatterns += router.urls
