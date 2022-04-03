from django.contrib.auth import get_user_model
from rest_framework import status, generics, response
from django.utils.translation import gettext_lazy as _

from .serializers import CountryAllFieldsSerializer, CityAllFieldsSerializer
from base.permissions import IsSuperuser
from .models import Country, City
from base.messages import DESTROY_SUCCEFUL

User = get_user_model()


class CountryCreateView(generics.CreateAPIView):
    """
    Cоздание нового объекта страны.
    """
    serializer_class = CountryAllFieldsSerializer
    permission_classes = (IsSuperuser, )


class CountryListView(generics.ListAPIView):
    """
    Просмотр списка стран.
    """
    serializer_class = CountryAllFieldsSerializer
    permission_classes = (IsSuperuser, )
    queryset = Country.objects.all()


class CountryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Просмотр, изменение и удаление отдельного объекта страны.
    """
    serializer_class = CountryAllFieldsSerializer
    permission_classes = (IsSuperuser, )
    queryset = Country.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        data = self.perform_destroy(instance)
        if not data:
            data = DESTROY_SUCCEFUL
        return response.Response(data=data, status=status.HTTP_204_NO_CONTENT)


class CityCreateView(generics.CreateAPIView):
    """
    Cоздание нового объекта города.
    """
    serializer_class = CityAllFieldsSerializer
    permission_classes = (IsSuperuser, )


class CityListView(generics.ListAPIView):
    """
    Просмотр списка городов.
    """
    serializer_class = CityAllFieldsSerializer
    permission_classes = (IsSuperuser, )
    queryset = City.objects.all()


class CityRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Просмотр, изменение и удаление отдельного объекта страны.
    """
    serializer_class = CityAllFieldsSerializer
    permission_classes = (IsSuperuser, )
    queryset = City.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        data = self.perform_destroy(instance)
        if not data:
            data = DESTROY_SUCCEFUL
        return response.Response(data=data, status=status.HTTP_204_NO_CONTENT)
