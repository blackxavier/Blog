from django.contrib import admin
from blog_app.models import PostModel, CategoryModel


@admin.register(PostModel)
class PostModelAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "id",
        "status",
        "slug",
        "author",
    )
    prepopulated_fields = {
        "slug": ("title",),
    }
    fieldsets = (
        (
            "Create Blog Post",
            {
                "fields": (
                    "title",
                    "slug",
                    "excerpt",
                    "content",
                )
            },
        ),
        ("Related Information", {"fields": ("author", "category", "tags")}),
        (
            "Other Information",
            {
                "fields": (
                    "published_date",
                    "status",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            "Create Blog Post",
            {
                "fields": (
                    "title",
                    "slug",
                    "excerpt",
                    "content",
                )
            },
        ),
        ("Related Information", {"fields": ("author", "category", "tags")}),
        (
            "Other Information",
            {
                "fields": (
                    "published_date",
                    "status",
                )
            },
        ),
    )


@admin.register(CategoryModel)
class PostModelAdmin(admin.ModelAdmin):
    list_display = ("category_name",)
