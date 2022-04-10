from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profile
from datetime import datetime, timedelta
from django.utils.translation import gettext_lazy as _
import jwt
from fcmadmin.settings import SECRET_KEY, JWT_ACCESS_TTL, JWT_REFRESH_TTL, ALGORITHM
from django.contrib.auth.password_validation import validate_password
from base.services import delete_old_file
from rest_framework.exceptions import ValidationError

User = get_user_model()


class UserPasswordChangeSerializer(serializers.Serializer):
    oldPassword = serializers.CharField(required=True, write_only=True)
    newPassword = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        if not self.context['request'].user.check_password(data.get('oldPassword')):
            raise serializers.ValidationError({'old_password': _('Wrong password.')})
        if data.get('oldPassword') == data.get('newPassword'):
            raise serializers.ValidationError(_('New and old password match'))
        validate_password(data.get('newPassword'), self.context['request'].user)
        return data

    def update(self, instance, validated_data):
        instance.set_password(validated_data['newPassword'])
        instance.save()
        return instance

    @property
    def data(self):
        # just return success dictionary.
        # you can change this to your need, but i dont think output should be user data after password change
        return {_("Password changed successfully")}


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Класс CustomUser.
    """
    # ==== OUTPUT ====
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
    )
    lastLogin = serializers.CharField(source='last_login', required=False)
    isActive = serializers.CharField(source='is_active', required=False)

    class Meta:
        model = User
        exclude = ("last_login", "is_active", "groups", "user_permissions")

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def get_isActive(self):
        return self.is_active

    def get_lastLogin(self):
        return self.last_login


class ProfileDetailSerializer(serializers.ModelSerializer):
    """
    Сериализатор для класса Profile. Используем все поля класса.
    """
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'

    def validate_birthdate(self, value):
        if self.instance.birthdate is not None and self.instance.birthdate != value:
            raise ValidationError(_('This field can only be changed once.'))
        return value

    def update(self, instance, validated_data):
        if validated_data.get('photo') is True:
            delete_old_file(instance.photo.path)
        return super().update(instance, validated_data)


class ProfilePhotoFIOSerializer(serializers.ModelSerializer):
    """
    Профиль - только фото и ФИО.
    """
    class Meta:
        model = Profile
        fields = ('photo', 'name', 'surname', 'patronymic')


class LoginSerializer(serializers.Serializer):
    """
    Сериализатор для генерации токенов.
    Сериализатор принимает емайл и пароль и возвращает пару токенов.
    """
    # ==== INPUT ====
    email = serializers.EmailField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)
    # ==== OUTPUT ====
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, attrs):
        # standard validation
        validated_data = super().validate(attrs)

        # validate email and password
        email = validated_data['email']
        password = validated_data['password']
        error_msg = _('email or password are incorrect')
        try:
            user = User.objects.get(email=email)
            if not user.check_password(password):
                raise serializers.ValidationError(error_msg)
            validated_data['user'] = user
        except User.DoesNotExist:
            raise serializers.ValidationError(error_msg)

        return validated_data

    def create(self, validated_data):
        access_payload = {
            'iss': 'fcm-backend-api',
            'user_id': validated_data['user'].id,
            'exp': datetime.utcnow() + timedelta(minutes=JWT_ACCESS_TTL),
            'type': 'access'
        }
        access = jwt.encode(payload=access_payload, key=SECRET_KEY, algorithm=ALGORITHM)

        refresh_payload = {
            'iss': 'fcm-backend-api',
            'userId': validated_data['user'].id,
            'exp': datetime.utcnow() + timedelta(minutes=JWT_REFRESH_TTL),
            'type': 'refresh'
        }
        refresh = jwt.encode(payload=refresh_payload, key=SECRET_KEY, algorithm=ALGORITHM)

        return {
            'access': access,
            'refresh': refresh
        }


class RefreshSerializer(serializers.Serializer):
    """
    Сериализатор для сброса токенов.
    Сериализатор принимает рефреш-токен и возвращает пару токенов.
    """
    # ==== INPUT ====
    refreshToken = serializers.CharField(required=True, write_only=True)
    # ==== OUTPUT ====
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    profile = ProfileDetailSerializer(read_only=True)

    def validate(self, attrs):
        # standard validation
        validated_data = super().validate(attrs)

        # validate refresh
        refresh_token = validated_data['refreshToken']
        try:
            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=ALGORITHM)
            if payload['type'] != 'refresh':
                error_msg = {'refreshToken': _('Token type is not refresh!')}
                raise serializers.ValidationError(error_msg)
            validated_data['payload'] = payload
        except jwt.ExpiredSignatureError:
            error_msg = {'refreshToken': _('Refresh token is expired!')}
            raise serializers.ValidationError(error_msg)
        except jwt.InvalidTokenError as e:
            print(e)
            error_msg = {'refreshToken': _('Refresh token is invalid!')}
            raise serializers.ValidationError(error_msg)

        return validated_data

    def create(self, validated_data):
        access_payload = {
            'iss': 'backend-api',
            'userId': validated_data['payload']['user_id'],
            'exp': datetime.utcnow() + timedelta(minutes=JWT_ACCESS_TTL),
            'type': 'access'
        }
        access = jwt.encode(payload=access_payload, key=SECRET_KEY, algorithm=ALGORITHM)

        refresh_payload = {
            'iss': 'backend-api',
            'userId': validated_data['payload']['userId'],
            'exp': datetime.utcnow() + timedelta(minutes=JWT_REFRESH_TTL),
            'type': 'refresh'
        }
        refresh = jwt.encode(payload=refresh_payload, key=SECRET_KEY, algorithm=ALGORITHM)

        user = validated_data['payload']['userId']
        profile = Profile.objects.get(user=user)
        serialized_profile = ProfileDetailSerializer(profile)

        return {
            'access': access,
            'refresh': refresh,
            'profile': serialized_profile.data,
        }


class UserListSerializer(serializers.ModelSerializer):
    """
    Данные о пользователе для вывода в списке пользователей.
    """
    lastLogin = serializers.CharField(source='last_login')
    isActive = serializers.CharField(source='is_active')

    class Meta:
        model = User
        exclude = ("last_login", "is_active", "password")

    def get_isActive(self):
        return self.is_active

    def get_lastLogin(self):
        return self.last_login