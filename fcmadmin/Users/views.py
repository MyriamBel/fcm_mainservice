# from psycopg2 import IntegrityError

from .api_shemas import login_schema, token_refresh_schema

# Сериализаторы пользователя
from .serializers import UserDetailSerializer, UserPasswordChangeSerializer, UserListSerializer
from .serializers import ProfileDetailSerializer  # Сериализаторы профиля
from .serializers import LoginSerializer, RefreshSerializer  # Сериализаторы генерации токенов

from rest_framework.response import Response
from rest_framework import status, generics, permissions, parsers, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import AuthenticationFailed, ValidationError

from .models import Profile

from base.permissions import IsSuperuser

from base.paginators import Standard10ResultsSetPagination

from drf_yasg.utils import swagger_auto_schema

from django.contrib.auth import get_user_model


User = get_user_model()


class UserCreateView(generics.CreateAPIView):
    """
    Cоздание нового пользователя при базовой регистрации -
    только администратор fcm или уже зарегистрированный пользователь может создать нового пользователя.
    """
    serializer_class = UserDetailSerializer
    permission_classes = (permissions.IsAuthenticated, IsSuperuser, )


class UserListView(generics.ListAPIView):
    """
    Список пользователей.
    """
    serializer_class = UserListSerializer
    queryset = User.objects.all()
    permission_classes = (IsSuperuser, )
    paginators = (Standard10ResultsSetPagination, )


class UserUpdatePasswordView(generics.UpdateAPIView):
    """
    Изменение пароля у пользователя.
    """
    serializer_class = UserPasswordChangeSerializer
    permission_classes = (permissions.IsAuthenticated, IsSuperuser, )

    def get_object(self, queryset=None):
        return self.request.user


class ProfileDetailView(generics.RetrieveAPIView):
    """
    Просмотр профиля - только для аутентифицированного пользователя,
    профиль извлекается тот, который привязан к пользователю.
    """
    serializer_class = ProfileDetailSerializer
    permission_classes = (permissions.IsAuthenticated, IsSuperuser, )

    # Извлекаем профиль, привязанный к пользователю
    def get_queryset(self):
        user = User.objects.get(email=self.request.user)
        profile = Profile.objects.get(user=user)
        return profile

    def get_object(self):
        return self.get_queryset()


class UserDetailProfile(generics.UpdateAPIView):
    """
    Просмотр и редактирование данных профиля пользователя.
    """
    parser_classes = (parsers.MultiPartParser,)
    serializer_class = ProfileDetailSerializer
    permission_classes = (permissions.IsAuthenticated, IsSuperuser, )

    def get_queryset(self):
        user = User.objects.get(email=self.request.user)
        profile = Profile.objects.get(user=user)
        return profile

    def get_object(self):
        return self.get_queryset()


@swagger_auto_schema(method='post', request_body=login_schema)
@api_view(["POST"])
def user_login(request, format=None):
    """
    Авторизация пользователя, авторизованному пользователю выдаются токены.
    """
    serializer = LoginSerializer(data=request.data)
    # Проверим валидность данных, переданных нам клиентской стороной.
    # Данные валидны - работаем дальше. Данные невалидны - возвращаем ошибку запроса
    if serializer.is_valid():
        response_data = serializer.save()
        return Response(response_data)
    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='post', request_body=token_refresh_schema)
@api_view(["POST"])
def user_refresh(request, format=None):
    """
    Обновление пары токенов с помощью прежнего рефреш-токена.
    """
    serializer = RefreshSerializer(data=request.data)
    # Проверим валидность данных, переданных нам клиентской стороной.
    # Данные валидны - работаем дальше. Данные невалидны - возвращаем ошибку запроса
    if serializer.is_valid():
        response_data = serializer.save()
        return Response(response_data)
    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
