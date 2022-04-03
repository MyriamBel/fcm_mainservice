from django.shortcuts import render
from rest_framework import parsers, generics, response, status, exceptions, permissions
from .serializer import FranchiseFoundersSerializer
from .serializer import CompanyFoundersSerializer
from .serializer import ServicePlaceFoundersSerializer
from .models import FranchiseFounders, CompanyFounders, ServicePlaceFounders
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
    queryset = ServicePlaceFounders
    serializer_class = ServicePlaceFoundersSerializer
    permission_classes = (IsSuperuser, )


class ServicePlaceFoundersListView(generics.ListAPIView):
    """
    Список учётных записей создателей объектов обслуживания.
    """
    queryset = ServicePlaceFounders
    serializer_class = ServicePlaceFoundersSerializer
    permission_classes = (IsSuperuser, )
