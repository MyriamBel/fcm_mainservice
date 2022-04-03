import hashlib
import uuid

from rest_framework import serializers, exceptions
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .models import ServicePlace, Terminal, Company
import jwt
from fcmadmin.settings import SECRET_KEY, ALGORITHM
from base.generators import decrypt_string
from django.core.exceptions import ValidationError

from .models import Franchise


User = get_user_model()


class FranchiseAllFieldsSerializer(serializers.ModelSerializer):
    """
    Франшиза - все поля.
    """

    class Meta:
        model = Franchise
        fields = '__all__'


class TerminalSerializer(serializers.Serializer):
    """
    Терминалы.
    """

    class Meta:
        model = Terminal
        fields = '__all__'


class ServicePlaceTerminalRegistrationSerializer(serializers.Serializer):
    """
    Регистрация терминала в торговых точках.
    """
    # ==== INPUT ====
    loginCheckoutTerminal = serializers.CharField(required=True, write_only=True)
    passwordCheckoutTerminal = serializers.CharField(required=True, write_only=True)
    deviceManufacturer = serializers.CharField(required=True, write_only=True)
    deviceModel = serializers.CharField(required=True, write_only=True)
    deviceSerialNumber = serializers.CharField(required=True, write_only=True)
    deviceIMEI = serializers.CharField(required=True, write_only=True)
    terminalSubtype = serializers.CharField(required=True, write_only=True)
    # ==== OUTPUT ====
    terminalToken = serializers.CharField(read_only=True)
    servicePlace = serializers.PrimaryKeyRelatedField(read_only=True)

    def validate(self, attrs):
        # standard validation
        validated_data = super().validate(attrs)

        # validate data
        loginCheckoutTerminal = validated_data['loginCheckoutTerminal']
        passwordCheckoutTerminal = validated_data['passwordCheckoutTerminal']
        deviceManufacturer = validated_data['deviceManufacturer']
        deviceModel = validated_data['deviceModel']
        deviceSerialNumber = validated_data['deviceSerialNumber']
        deviceIMEI = validated_data['deviceIMEI']
        terminalSubtype = validated_data['terminalSubtype']

        print(validated_data)

        error_msg = _('login or password are incorrect')
        try:
            servicePlace = ServicePlace.objects.get(loginCheckoutTerminal=loginCheckoutTerminal)
            if not servicePlace.check_password(loginCheckoutTerminal, passwordCheckoutTerminal):
                raise serializers.ValidationError(error_msg)
            validated_data['servicePlace'] = servicePlace.pk
            validated_data['passwordCheckoutTerminal'] = passwordCheckoutTerminal
        except ServicePlace.DoesNotExist:
            raise serializers.ValidationError(error_msg)

        return validated_data

    def create(self, validated_data):
        object = Terminal(servicePlace=ServicePlace.objects.get(pk=self.validated_data['servicePlace']))
        object.deviceModel = validated_data["deviceModel"]
        object.deviceSerialNumber = validated_data["deviceSerialNumber"]
        object.deviceIMEI = validated_data["deviceIMEI"]
        object.deviceManufacturer = validated_data["deviceManufacturer"]
        try:
            object.save(**validated_data)
        except ValidationError as e:
            raise exceptions.ValidationError(e.message)

        payload = {
            'iss': 'backend-api',
            'service_point_id': validated_data['servicePlace'],
            'terminal_id': object.pk,
            'terminal_type': validated_data['terminalSubtype'],
        }
        token = jwt.encode(payload=payload, key=SECRET_KEY, algorithm=ALGORITHM)
        object.token = token
        object.save()

        return {
            'terminalToken': token,
        }


class CompanySerializer(serializers.ModelSerializer):
    """
    Компании.
    """
    class Meta:
        model = Company
        fields = '__all__'


class ServicePlaceRegisterSerializer(serializers.ModelSerializer):
    """
    Точки обслуживания.
    """

    class Meta:
        model = ServicePlace
        exclude = ['passwordCheckoutTerminal', 'loginCheckoutTerminal']


class ServicePlaceTerminalsLoginPasswordSerializer(serializers.ModelSerializer):
    """
    # Только логин и пароль регистрации терминала.
    """
    class Meta:
        model = ServicePlace
        fields = ['passwordCheckoutTerminal', 'loginCheckoutTerminal']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['passwordCheckoutTerminal'] = decrypt_string(representation['passwordCheckoutTerminal'])
        return representation







