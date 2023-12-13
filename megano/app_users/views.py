import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserAvatar, UserProfile
from .serializers import (
    SignUpSerializer,
    ProfileSerializer,
    PasswordUpdateSerializer,
    AvatarSerializer,
)


class SignInView(APIView):
    def post(self, request: Request) -> Response:
        try:
            user_data = json.loads(next(iter(request.data.keys())))
            username = user_data.get("username")
            password = user_data.get("password")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return Response(status=status.HTTP_200_OK)

            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except json.JSONDecodeError:
            return Response(
                status=status.HTTP_400_BAD_REQUEST, data={"error": "Invalid JSON data"}
            )


class SignUpView(APIView):
    @transaction.atomic
    def post(self, request: Request, *args, **kwargs) -> Response:
        # Преобразуем строку JSON в словарь
        json_data = list(request.data.keys())[0]
        data_dict = json.loads(json_data)

        # Передаем словарь данных напрямую в сериализатор
        serializer = SignUpSerializer(data=data_dict)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            name, username, password = (
                validated_data["name"],
                validated_data["username"],
                validated_data["password"],
            )

            try:
                # Create user, avatar, and profile
                user = User.objects.create_user(username=username, password=password)
                avatar = UserAvatar.objects.create(alt=f"{name}'s Avatar")
                profile = UserProfile.objects.create(
                    user=user, full_name=name, avatar=avatar
                )

                # Authenticate and login
                user = authenticate(request, username=username, password=password)
                if user:
                    login(request, user)

                return Response(status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response(
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={"error": str(e)}
                )
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST, data={"errors": serializer.errors}
            )


class SignOutView(APIView):
    def post(self, request: Request) -> Response:
        logout(request)
        return Response(status=status.HTTP_200_OK)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get(self, request: Request) -> Response:
        profile = get_object_or_404(UserProfile, user=request.user)
        serializer = self.serializer_class(profile)

        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        profile = get_object_or_404(UserProfile, user=request.user)
        serializer = self.serializer_class(profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AvatarUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def post(self, request: Request, *args, **kwargs) -> Response:
        """Updates the user's avatar."""
        try:
            avatar = request.user.profile.avatar

            if "avatar" in request.FILES:
                # Удаление старого файла перед сохранением нового
                if avatar.src:
                    avatar.src.delete()

                avatar.src = request.FILES["avatar"]
                avatar.save()

                return Response(status=status.HTTP_200_OK)

            return Response(
                {"error": "No 'avatar' file provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PasswordUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def get_user(self):
        return self.request.user

    def post(self, request: Request) -> Response:
        serializer = PasswordUpdateSerializer(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            user = self.get_user()
            new_password = serializer.validated_data["newPassword"]

            user.set_password(new_password)
            user.save()

            return Response(status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
