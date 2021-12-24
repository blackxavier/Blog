from django.urls import path
from blog_api.views import PostListView, CategoryViewset, CommentCreateReadView
from rest_framework.routers import SimpleRouter

app_name = "blog_api"


router = SimpleRouter()
router.register(r"categories", CategoryViewset, basename="category")
urlpatterns = [
    path("posts/", PostListView.as_view(), name="post_list"),
    path(
        "posts/<int:pk>/comments/",
        CommentCreateReadView.as_view(),
        name="comment-list-create",
    ),
]
urlpatterns += router.urls
