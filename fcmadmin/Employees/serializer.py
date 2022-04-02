from rest_framework import serializers, exceptions
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .models import FranchiseFounders, CompanyFounders, ServicePlaceFounders


user = get_user_model()


class FranchiseFoundersSerializer(serializers.ModelSerializer):
    """
    Сериализатор для объекта FranchiseFounders - учетной записи основателя франшизы.
    """

    class Meta:
        model = FranchiseFounders
        fields = "__all__"


class CompanyFoundersSerializer(serializers.ModelSerializer):
    """
    Сериализатор для объекта CompanyFounders - учётной записи основателя сети.
    """

    class Meta:
        model = CompanyFounders
        fields = "__all__"


class ServicePlaceFoundersSerializer(serializers.ModelSerializer):
    """
    Сериализатор для объекта ServicePlaceFounders - учётной записи основателя объекта обслуживания.
    """

    class Meta:
        model = ServicePlaceFounders
        fields = "__all__"
