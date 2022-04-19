import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from users.manager import CustomUserManager


class User(AbstractUser):
    username = models.CharField(_("Username "), max_length=256, unique=True)
    email = models.EmailField(_("email address"), unique=True)
    about_user = models.TextField(_("About user"))
    identifier = models.UUIDField(default=uuid.uuid4, editable=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email
