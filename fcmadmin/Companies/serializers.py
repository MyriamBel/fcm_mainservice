from rest_framework import serializers, exceptions
from django.contrib.auth import get_user_model

from .models import Franchise


User = get_user_model()


class FranchiseAllFieldsSerializer(serializers.ModelSerializer):
    """
    Франшиза - все поля.
    """

    class Meta:
        model = Franchise
        fields = '__all__'
