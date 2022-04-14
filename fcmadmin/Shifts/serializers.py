import jwt
from rest_framework import serializers, exceptions
from django.utils.translation import gettext_lazy as _
from fcmadmin.settings import SECRET_KEY, ALGORITHM, JWT_ACCESS_TTL, JWT_REFRESH_TTL
from Employees.models import Cashier
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model

user = get_user_model()


class StaffDeviceLoginSerializer(serializers.Serializer):
    """
    Авторизация пользователя на определенном устройстве.
    """
    # ===INPUT===
    terminalToken = serializers.CharField(max_length=250, required=True, write_only=True)
    userPin = serializers.CharField(max_length=4, required=True, write_only=True)
    # ===OUTPUT===
    authorizeToken = serializers.CharField(max_length=250, read_only=True)

    def validate(self, attrs):
        validated_data = super(StaffDeviceLoginSerializer, self).validate(attrs)
        terminalToken = validated_data.pop("terminalToken")
        userPin = validated_data.pop("userPin")
        print(userPin)
        try:
            payload = jwt.decode(terminalToken, key=SECRET_KEY, algorithms=ALGORITHM)
        except jwt.PyJWTError:
            raise exceptions.AuthenticationFailed('Invalid authentication. Could not decode terminal'
                                                  ' token.')
        servicePlace = payload["service_point_id"]
        staff = set()
        for child in Cashier.__subclasses__():
            try:
                cashier = child.objects.filter(servicePlace=servicePlace).get(pin=userPin)
                staff.add(cashier)
            except child.DoesNotExist:
                pass
        if not staff:
            raise exceptions.AuthenticationFailed(_("Staff with this pin not found. "
                                                    "Check your pin or contact the administrator."))
        validated_data["userPin"] = userPin
        validated_data["servicePlace"] = servicePlace
        validated_data["user_id"] = staff.pop().user.pk
        return validated_data

    def create(self, validated_data):
        access_payload = {
            'iss': 'fcm-backend-api',
            'userPin': validated_data['userPin'],
            "user_id": validated_data["user_id"],
            'servicePlace': validated_data['servicePlace'],
            'exp': datetime.utcnow() + timedelta(minutes=JWT_ACCESS_TTL),
            'type': 'access'
        }
        access = jwt.encode(payload=access_payload, key=SECRET_KEY, algorithm=ALGORITHM)

        refresh_payload = {
            'iss': 'fcm-backend-api',
            'userPin': validated_data['userPin'],
            "user_id": validated_data["user_id"],
            'servicePlace': validated_data['servicePlace'],
            'exp': datetime.utcnow() + timedelta(minutes=JWT_REFRESH_TTL),
            'type': 'refresh'
        }
        refresh = jwt.encode(payload=refresh_payload, key=SECRET_KEY, algorithm=ALGORITHM)

        return {
            'access': access,
            'refresh': refresh
        }


class StaffDeviceRefreshSerializer(serializers.Serializer):
    """
    Рефреш пары токенов.
    """
    # ==== INPUT ====
    terminalToken = serializers.CharField(max_length=250, required=True, write_only=True)
    refreshToken = serializers.CharField(required=True, write_only=True)
    # ==== OUTPUT ====
    authorizeToken = serializers.CharField(max_length=250, read_only=True)

    def validate(self, attrs):
        # standard validation
        validated_data = super().validate(attrs)

        # validate refresh
        refresh_token = validated_data['refreshToken']
        terminalToken = validated_data["terminalToken"]
        try:
            payloadTerminal = jwt.decode(terminalToken, key=SECRET_KEY, algorithms=ALGORITHM)
        except jwt.PyJWTError:
            raise exceptions.AuthenticationFailed('Invalid authentication. Could not decode '
                                                  'terminal token.')
        servicePlace = payloadTerminal["service_point_id"]
        try:
            payload = jwt.decode(refresh_token, key=SECRET_KEY, algorithms=ALGORITHM)
            if payload['type'] != 'refresh':
                error_msg = {'refreshToken': _('Token type is not refresh!')}
                raise serializers.ValidationError(error_msg)
        except jwt.ExpiredSignatureError:
            error_msg = {'refreshToken': _('Refresh token is expired!')}
            raise serializers.ValidationError(error_msg)
        except jwt.InvalidTokenError:
            error_msg = {'refreshToken': _('Refresh token is invalid!')}
            raise serializers.ValidationError(error_msg)
        except jwt.PyJWTError:
            raise exceptions.AuthenticationFailed('Invalid authentication. Could not decode token.')
        if payload["servicePlace"] != servicePlace:
            raise serializers.ValidationError("This token not for this place.")
        validated_data = payload
        validated_data["user_id"] = payload["user_id"]
        return validated_data

    def create(self, validated_data):
        access_payload = {
                'iss': 'fcm-backend-api',
                # 'user_id': ''
                'userPin': validated_data['userPin'],
            "user_id": validated_data["user_id"],
            'servicePlace': validated_data['servicePlace'],
                'exp': datetime.utcnow() + timedelta(minutes=JWT_ACCESS_TTL),
                'type': 'access'
        }
        access = jwt.encode(payload=access_payload, key=SECRET_KEY, algorithm=ALGORITHM)

        refresh_payload = {
                'iss': 'fcm-backend-api',
                'userPin': validated_data['userPin'],
                "user_id": validated_data["user_id"],
                'servicePlace': validated_data['servicePlace'],
                'exp': datetime.utcnow() + timedelta(minutes=JWT_REFRESH_TTL),
                'type': 'refresh'
        }
        refresh = jwt.encode(payload=refresh_payload, key=SECRET_KEY, algorithm=ALGORITHM)

        return {
                'access': access,
                'refresh': refresh
        }