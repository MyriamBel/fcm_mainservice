from rest_framework import serializers, exceptions
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .models import Country, City

User = get_user_model()


class CountryNameSerializer(serializers.ModelSerializer):
    """
    Название страны.
    """
    class Meta:
        model = Country
        fields = ('name', )


class CountryAllFieldsSerializer(CountryNameSerializer):
    """
    Класс Страна.
    """
    class Meta:
        model = Country
        fields = '__all__'


class CityNameFieldSerializer(serializers.ModelSerializer):
    """
    Город - только название.
    """

    class Meta:
        model = City
        fields = ('name',)


class CityAllFieldsSerializer(CityNameFieldSerializer):
    """
    Класс Город.
    """
    class Meta:
        model = City
        fields = '__all__'
