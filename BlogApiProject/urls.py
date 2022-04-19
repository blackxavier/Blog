from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("blog_api.urls", namespace="blog_api")),
    path("", include("users.urls", namespace="users")),
    path("__debug__/", include("debug_toolbar.urls")),
]
