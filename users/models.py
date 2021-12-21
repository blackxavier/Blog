from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from users.manager import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    """[This class subclasses from 'AbstractBaseUser' and 'PermissionsMixin' and creates a custom user model.]

    Args:
        AbstractBaseUser ([User object]): [returns a user object]
        PermissionsMixin ([Permission object]): [return a permission object related to the user]

    Returns:
        [User object]: [creates and return user object]
    """

    email = models.EmailField(_("Email Address"), unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    date_created = models.DateTimeField(default=timezone.now)
    about_user = models.TextField(_("About"), max_length=500, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return f"User - {self.email}"
