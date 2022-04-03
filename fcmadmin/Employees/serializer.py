from rest_framework import serializers, exceptions
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .models import FranchiseFounders, CompanyFounders, ServicePlaceFounders
from django.core.exceptions import ValidationError


user = get_user_model()


class BaseSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор для всех профилей. Здесь определим общие для всех методы.
    """
    def create(self, validated_data):
        try:
            self.Meta.model.objects.create(**validated_data)
        except ValidationError as e:
            raise exceptions.ValidationError(e.message)


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


class ServicePlaceFoundersSerializer(BaseSerializer):
    """
    Сериализатор для объекта ServicePlaceFounders - учётной записи основателя объекта обслуживания.
    """

    class Meta:
        model = ServicePlaceFounders
        fields = "__all__"


