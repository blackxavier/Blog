from django.urls import path

from users.views import (ChangePasswordView, ObtainAuthTokenView,
                         RegistrationView, UserProfileView, user_logout)

app_name = "users"

urlpatterns = [
    path("auth/register/", RegistrationView.as_view(), name="register"),
    path("auth/login/", ObtainAuthTokenView.as_view(), name="login"),
    path("auth/logout/", user_logout, name="logout"),
    path("auth/change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("me/", UserProfileView, name="user-details"),
]
