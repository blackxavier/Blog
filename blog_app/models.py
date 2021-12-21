from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.conf import settings
from taggit.managers import TaggableManager

user = get_user_model()


class CategoryModel(models.Model):
    category_name = models.CharField(max_length=200)

    class Meta:

        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category_name


class PostModel(models.Model):
    class PublishedPost(models.Manager):
        """Custom model manager for published posts"""

        def get_queryset(self):
            return super().get_queryset().filter(status="published")

    class DraftedPost(models.Manager):
        """Custom model manager for drafted posts"""

        def get_queryset(self):
            return super().get_queryset().filter(status="draft")

    blog_options = (("draft", "Draft"), ("published", "Published"))
    category = models.ForeignKey(CategoryModel, on_delete=models.PROTECT, default=1)
    title = models.CharField(max_length=250)
    excerpt = models.TextField(null=True)
    content = models.TextField()
    slug = models.SlugField(max_length=250, unique_for_date="published_date")
    published_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(
        user, on_delete=models.CASCADE, related_name="blog_posts"
    )
    status = models.CharField(max_length=10, choices=blog_options, default="draft")

    objects = models.Manager()
    publishedpost = PublishedPost()
    draftedpost = DraftedPost()
    tags = TaggableManager()

    class Meta:

        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ("-published_date",)

    def __str__(self):
        return f"Title of post - {self.title}"
