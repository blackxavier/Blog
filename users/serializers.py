from django.contrib.auth import authenticate, get_user_model
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, status

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):

    confirm_password = serializers.CharField(
        style={"input_type": "password"},
        write_only=True,
    )

    class Meta:
        model = User
        fields = ["email", "password", "username", "confirm_password"]
        extra_kwargs = {"password": {"write_only": True}}

    def save(self):
        account = User(
            email=self.validated_data["email"], username=self.validated_data["username"]
        )
        password = self.validated_data["password"]
        confirm_password = self.validated_data["confirm_password"]

        if password != confirm_password:
            raise serializers.ValidationError(
                {"password": "Passwords must match"}, code="authorization"
            )
        else:
            account.set_password(password)
            account.save()
            return account


class ReadUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "pk",
            "email",
            "username",
            "first_name",
            "about_user",
            "date_joined",
            "is_active",
        ]


class WriteUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "about_user"]


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(label=_("Email"), write_only=True)
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )
    token = serializers.CharField(label=_("Token"), read_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get("request"), username=email, password=password
            )

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    @transaction.atomic()
    def validate(self, attrs):
        obj = self.context["request"].user
        old_password = attrs["old_password"]
        print(old_password)
        if not obj.check_password(old_password):
            raise serializers.ValidationError(
                {"old_password": ["Wrong password."]},
                status.HTTP_400_BAD_REQUEST,
            )
        # confirm the new passwords match
        new_password = attrs["new_password"]
        confirm_new_password = attrs["confirm_new_password"]
        if new_password != confirm_new_password:

            raise serializers.ValidationError(
                {"new_password": ["New passwords does not match"]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        obj.set_password(new_password)
        obj.save(update_fields=["password"])
        return attrs

    def save(self):
        obj = self.context["request"].user
        # set_password also hashes the password that the user will get
        obj.set_password(self.validated_data["new_password"])
        obj.save(update_fields=["password"])
