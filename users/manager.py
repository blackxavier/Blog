from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of usernames.
    """

    def create_user(self, email, username, password, **other_fields):
        """[creates and saves a user]

        Args:
            email ([EmailField]): [This field stores email]
            username ([CharField]): [This field stores username]
            password ([CharField]): [This fied stores password]

        Raises:
            ValueError: [Raises ValueError if email is not included]

        Returns:
            [User object]: [Returns a user object after succssfully creating a user]
        """
        if not email:
            raise ValueError(_("You must include an email address"))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **other_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, username, password, **other_fields):
        """[creates and saves a superuser]

        Args:
            email ([EmailField]): [This field stores email]
            username ([CharField]): [This field stores username]
            password ([CharField]): [This fied stores password]

        Raises:
            ValueError: [Raises ValueError if email is not included]
            ValueError: [Raises ValueError if 'superuser' is not set to True]
            ValueError: [Raises ValueError if 'is_staff' is not set to True]
            ValueError: [Raises ValueError if 'is_active' is not set to True]

        Returns:
            [User object]: [Returns a user object after succssfully creating a superuser]
        """
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_active", True)
        other_fields.setdefault("is_superuser", True)
        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be assigned to 'is_staff=True' ")
        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must be assigned to 'is_superuser=True' ")
        return self.create_user(email, username, password, **other_fields)
