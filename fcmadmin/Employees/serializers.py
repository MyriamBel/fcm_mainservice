from django.db import IntegrityError
from rest_framework import serializers, exceptions
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .models import FranchiseFounders, CompanyFounders, ServicePlaceFounders
from .models import ServicePlaceBarista
from Companies.models import ServicePlace


user = get_user_model()


class BaseSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор для всех профилей. Здесь определим общие для всех методы.
    """
    
    def validate(self, attrs):
        return super(BaseSerializer, self).validate(attrs)

    def create(self, validated_data):
        if self.is_valid(raise_exception=True):
            try:
                return self.Meta.model.objects.create(**validated_data)
            except IntegrityError as e:
                raise exceptions.ValidationError(e)

    def update(self, instance, validated_data):
        if self.is_valid(raise_exception=True):
            try:
                return self.Meta.model.objects.update(**validated_data)
            except IntegrityError as e:
                raise exceptions.ValidationError(e)


class ServicePlaceEmloyeesSerializer(BaseSerializer):
    """
    Сериализатор для сотрудников точки обслуживания.
    """
    servicePlace = serializers.PrimaryKeyRelatedField(queryset=ServicePlace.objects.all())


class FranchiseFoundersSerializer(BaseSerializer):
    """
    Сериализатор для объекта FranchiseFounders - учетной записи основателя франшизы.
    """

    class Meta:
        model = FranchiseFounders
        fields = "__all__"


class CompanyFoundersSerializer(BaseSerializer):
    """
    Сериализатор для объекта CompanyFounders - учётной записи основателя сети.
    """

    class Meta:
        model = CompanyFounders
        fields = "__all__"


class ServicePlaceFoundersSerializer(ServicePlaceEmloyeesSerializer):
    """
    Сериализатор для объекта ServicePlaceFounders - учётной записи основателя объекта обслуживания.
    """

    class Meta:
        model = ServicePlaceFounders
        fields = "__all__"


class ServicePlaceBaristaSerializer(ServicePlaceEmloyeesSerializer):
    """
    Сериализатор для объекта ServicePlaceBarista - учётной записи бариста в заведении. Бариста может иметь право
    работать с кассой - булево поле isCashier.
    """
    barista = serializers.PrimaryKeyRelatedField(queryset=user.objects.all())

    class Meta:
        model = ServicePlaceBarista
        fields = "__all__"







