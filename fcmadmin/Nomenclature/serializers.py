from rest_framework import serializers
from models import DishCategory, DishSubCategory
from django.contrib.auth import get_user_model

User = get_user_model()


class DishCategoryNameImageFieldsSerializer(serializers.ModelSerializer):
    """
    Сериализатор меню - только поля с нгазванием пункта и картинкой.
    """
    class Meta:
        model = DishCategory
        fields = ['name', 'image']

