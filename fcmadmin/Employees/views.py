from django.shortcuts import render
from rest_framework import parsers, generics, response, status, exceptions, permissions
from .serializers import FranchiseFoundersSerializer
from .serializers import CompanyFoundersSerializer
from .serializers import ServicePlaceFoundersSerializer
from .models import FranchiseFounders, CompanyFounders, ServicePlaceFounders
from .models import ServicePlaceBarista
from .serializers import ServicePlaceBaristaSerializer
from base.permissions import IsSuperuser


class FranchiseFounderCreateView(generics.CreateAPIView):
    """
    Создание учетной записи основателя франшизы.
    """
    serializer_class = FranchiseFoundersSerializer
    queryset = FranchiseFounders.objects.all()
    permission_classes = (IsSuperuser, )


class FranchiseFounderListView(generics.ListAPIView):
    """
    Список основаталей франшиз.
    """
    serializer_class = FranchiseFoundersSerializer
    queryset = FranchiseFounders.objects.all()
    permission_classes = (IsSuperuser, )


class CompanyFounderCreateView(generics.CreateAPIView):
    """
    Создание учетной записи основателя сети.
    """
    queryset = CompanyFounders.objects.all()
    serializer_class = CompanyFoundersSerializer
    permission_classes = (IsSuperuser, )


class CompanyFounderListView(generics.ListAPIView):
    """
    Список основателей сети.
    """
    queryset = CompanyFounders.objects.all()
    serializer_class = CompanyFoundersSerializer
    permission_classes = (IsSuperuser, )


class ServicePlaceFoundersCreateView(generics.CreateAPIView):
    """
    Создание учётной записи создателя объекта обслуживания.
    """
    queryset = ServicePlaceFounders.objects.all()
    serializer_class = ServicePlaceFoundersSerializer
    permission_classes = (IsSuperuser, )


class ServicePlaceFoundersListView(generics.ListAPIView):
    """
    Список учётных записей создателей объектов обслуживания.
    """
    queryset = ServicePlaceFounders.objects.all()
    serializer_class = ServicePlaceFoundersSerializer
    permission_classes = (IsSuperuser, )


class ServicePlaceBaristaCreateView(generics.CreateAPIView):
    """
    Создание учётной записи бариста. Бариста может иметь право работать с кассой - за это отвечают
    булево поле isCashier и
    автоматически генерируемое поле pin.
    Чтобы получить пин-код сотрудника, нужно сначала присвоить ему право работы с кассой через поле isCashier,
    затем сохранить объект сотрудника. При этом сгенерируется пин-код, который можно будет уже получить.
    При последующих изменениях права работы с кассой пин-код сотрудника меняться не будет.
    """
    serializer_class = ServicePlaceBaristaSerializer
    permission_classes = (IsSuperuser, )
    queryset = ServicePlaceBarista.objects.all()


class ServicePlaceBaristaListView(generics.ListAPIView):
    """
    Список всех бариста.
    """
    serializer_class = ServicePlaceBaristaSerializer
    permission_classes = (IsSuperuser, )
    queryset = ServicePlaceBarista.objects.all()
