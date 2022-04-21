from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_save
from django.template.defaultfilters import slugify
from django.utils import timezone
from taggit.managers import TaggableManager

from blog_app.utils import get_random_string
from django.utils.translation import gettext_lazy as _

user = get_user_model()


class CategoryModel(models.Model):
    category_name = models.CharField(_("Category name"), max_length=200, unique=True)
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:

        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category_name


blog_options = (("draft", "Draft"), ("published", "Published"))


class PostModel(models.Model):
    class PublishedPost(models.Manager):
        """Custom model manager for published posts"""

        def get_queryset(self):
            return super().get_queryset().filter(status="published")

    class DraftedPost(models.Manager):
        """Custom model manager for drafted posts"""

        def get_queryset(self):
            return super().get_queryset().filter(status="draft")

    class BookmarkedPost(models.Manager):
        """Custom model manager for drafted posts"""

        def get_queryset(self):
            return super().get_queryset().filter(is_bookmarked=True)

    category = models.ForeignKey(
        CategoryModel, on_delete=models.PROTECT, default=1, related_name="related_posts"
    )
    title = models.CharField(_("Post title"), max_length=250)
    excerpt = models.TextField(_("Excerpt"))
    content = models.TextField(_("Content"))
    slug = models.SlugField(max_length=250, null=False, unique=True)
    published_date = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        user, on_delete=models.CASCADE, related_name="blog_posts"
    )

    status = models.CharField(
        _("Post status"), max_length=10, choices=blog_options, default="draft"
    )
    is_bookmarked = models.BooleanField(_("Bookmark this post"), default=False)

    objects = models.Manager()
    publishedpost = PublishedPost()
    draftedpost = DraftedPost()
    bookmarkedpost = BookmarkedPost()
    tags = TaggableManager()

    class Meta:

        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ("-published_date",)

    def __str__(self):
        return f"Title of post - {self.title}"


class CommentModel(models.Model):
    comment_text = models.TextField(_("comment text"))
    date_created = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey(
        PostModel, on_delete=models.CASCADE, related_name="comments"
    )
    is_active = models.BooleanField(_("active"), default=True)

    class Meta:

        verbose_name_plural = "Comments"

    def __str__(self):
        return f"Comment ID - {str(self.id)}"


def create_slug(instance, new_slug=None):
    """
    Create and validate slug duplication
    """
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    else:
        qs = PostModel.objects.filter(slug=slug).order_by("-id")
        exist = qs.exists()
        if exist:
            generated_string = get_random_string(4)
            slug = slug + "-" + generated_string
    return slug


def pre_save_post_reciever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_reciever, sender=PostModel)
