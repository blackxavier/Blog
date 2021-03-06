from django.urls import path
from rest_framework.routers import SimpleRouter

from blog_api.views import (
    AllPostDrafts,
    CategoryViewset,
    CommentCreateListReadView,
    PostCreateView,
    PostListView,
    PostRetrieveView,
    StatusChangePostView,
    ListTagsView,
    BookmarkPostView,
    AllBookmarkPostByUserView,
)

app_name = "blog_api"


router = SimpleRouter()
router.register(r"categories", CategoryViewset, basename="category")
urlpatterns = [
    path("posts/", PostListView.as_view(), name="post_list"),
    path("users/me/drafted-posts/", AllPostDrafts.as_view(), name="post_drafted"),
    path(
        "posts/<slug:slug>/publish/",
        StatusChangePostView.as_view(),
        name="post_publish",
    ),
    path(
        "posts/<slug:slug>/bookmark/",
        BookmarkPostView.as_view(),
        name="post_publish",
    ),
    path(
        "posts/bookmarks/",
        AllBookmarkPostByUserView.as_view(),
        name="post_publish",
    ),
    path("posts/create/", PostCreateView.as_view(), name="post_create"),
    path(
        "posts/<int:pk>/comments/",
        CommentCreateListReadView.as_view(),
        name="comment-list-create",
    ),
    path("tags/", ListTagsView.as_view(), name="tag"),
    path("posts/<slug:slug>/", PostRetrieveView.as_view(), name="post_detail"),
]
urlpatterns += router.urls
