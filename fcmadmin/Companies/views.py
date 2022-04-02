from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view

from .serializers import FranchiseAllFieldsSerializer, ServicePointTerminalRegistrationSerializer
from .serializers import ServicePlaceSerializer, CompanySerializer
from django.contrib.auth import get_user_model
from .models import Franchise, ServicePlace, Company
from rest_framework import parsers, generics, response, status, exceptions, permissions
from django.utils.translation import gettext_lazy as _
from base.paginators import Standard10ResultsSetPagination
from base.permissions import IsSuperuser
from .api_shemas import get_token_shema
from rest_framework.response import Response


User = get_user_model()


class FranchiseAddView(generics.CreateAPIView):
    """
    Создание сети/франшизы.
    """
    serializer_class = FranchiseAllFieldsSerializer
    permission_classes = (permissions.IsAuthenticated, )
    # parser_classes = (parsers.MultiPartParser, )
    queryset = Franchise.objects.all()


class ServicePlaceCreateView(generics.CreateAPIView):
    """
    Создание точки обслуживания.
    """
    serializer_class = ServicePlaceSerializer

    def get_object(self):
        return ServicePlace.objects.all()


class CompanyCreateView(generics.CreateAPIView):
    """
    Создание компании.
    """
    serializer_class = CompanySerializer

    def get_object(self):
        return Company.objects.all()


@swagger_auto_schema(method='post', request_body=get_token_shema)
@api_view(["POST"])
def servicePointCreatorView(request):
    """
    Регистрация приложения в торговой точке.
    Приходит логин и пароль заведения + информация устройства, на котором устанавливается терминал.
    Возвращается - уникальный токен для идентификации терминала.
    """
    serializer_class = ServicePointTerminalRegistrationSerializer(data=request.data)

    if serializer_class.is_valid():
        response_data = serializer_class.create(serializer_class.validated_data)
        return Response(response_data)
    return Response(data=serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)
