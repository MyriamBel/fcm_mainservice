from rest_framework import serializers
from .models import Menu, DishCategory, DishTags, Dish
from django.contrib.auth import get_user_model

User = get_user_model()


class MenuAllFieldsSerializer(serializers.ModelSerializer):
    """
    Сериализатор меню - все поля (для создания).
    """

    class Meta:
        model = Menu
        fields = "__all__"


class DishCategoryCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор категории - все поля (для создания).
    """

    class Meta:
        model = DishCategory
        fields = "__all__"


class DishTagsCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для тегов блюд.
    """

    class Meta:
        model = DishTags
        fields = "__all__"


class DishTagsListSerializer(serializers.ModelSerializer):
    """
    Сериализатор названия тега. Для вывода списка тегов в зависимости от выбранного пункта меню.
    """

    class Meta:
        model = DishTags
        fields = ["name", ]


class DishesCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для блюд.
    """
    class Meta:
        model = Dish
        fields = "__all__"


class DishCategoryImgNameFieldsSerializer(serializers.ModelSerializer):
    """
    Получить список категорий меню - только изображение и название поля.
    """

    class Meta:
        model = DishCategory
        fields = ["image", "name"]
