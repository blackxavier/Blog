from rest_framework import status, views, permissions
from rest_framework.response import Response
from users.serializers import (
    RegistrationSerializer,
    AuthTokenSerializer,
    ChangePasswordSerializer,
    ReadUserProfileSerializer,
    WriteUserSerializer,
)
from rest_framework.authtoken.models import Token
from django.db import transaction
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import get_user_model, logout
from rest_framework.generics import UpdateAPIView
from rest_framework.decorators import api_view, permission_classes


User = get_user_model()


class RegistrationView(views.APIView):
    permission_classes = [permissions.AllowAny]

    @transaction.atomic()
    def post(self, request):
        if request.method == "POST":
            serializer = RegistrationSerializer(data=request.data)
            if serializer.is_valid():
                account = serializer.save()
                token = Token.objects.create(user=account)
                data = {
                    "user": {
                        "email": account.email,
                    },
                    "response": "Account was successfuly created",
                    "status": f"{status.HTTP_201_CREATED} CREATED",
                    "Key": {
                        "token": token.key,
                    },
                }
                return Response(data)
            else:
                data = serializer.errors
                return Response(data)


class ObtainAuthTokenView(ObtainAuthToken):
    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(
            data=request.data, context={"request": request}
        )

        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        token, created = Token.objects.get_or_create(user=user)

        return Response({"token": token.key, "user_id": user.pk, "email": user.email})


class ChangePasswordView(UpdateAPIView):

    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    @transaction.atomic()
    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"response": "successfully changed password"}, status=status.HTTP_200_OK
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@transaction.atomic()
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def user_logout(request):

    request.user.auth_token.delete()

    logout(request)
    data = {
        "response": "User logged out successfully.",
        "status": f"{status.HTTP_200_OK} OK",
    }
    return Response(data)


@transaction.atomic
@api_view(["GET", "PUT", "PATCH"])
@permission_classes((permissions.IsAuthenticated,))
def UserProfileView(request):

    try:
        account = request.user
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ReadUserProfileSerializer(account)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = WriteUserSerializer(account, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data = {
                "data": ReadUserProfileSerializer,
                "response": "Account was updated successfully",
            }

            return Response(data=data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "PATCH":
        serializer = WriteUserSerializer(account, data=request.data, partial=True)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data = {
                "data": ReadUserProfileSerializer,
                "response": "Account was updated successfully",
            }
            return Response(data=data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
