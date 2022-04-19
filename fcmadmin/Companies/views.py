from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view

from .serializers import FranchiseAllFieldsSerializer
from .serializers import ServicePlaceTerminalRegistrationSerializer
from .serializers import ServicePlaceRegisterSerializer, ServicePlaceTerminalsLoginPasswordSerializer
from .serializers import CompanySerializer
from .serializers import RoomAllFieldSerializer

# from .serializers import ServicePlaceAllFieldsSerializer
from django.contrib.auth import get_user_model
from .models import Franchise, ServicePlace, Company
from .models import Terminal, Room
from rest_framework import parsers, generics, response, status, exceptions, permissions
from django.utils.translation import gettext_lazy as _
from base.paginators import Standard10ResultsSetPagination
from base.permissions import IsSuperuser, IsCashier
from .api_shemas import get_token_shema
from rest_framework.response import Response


User = get_user_model()


class RoomCreateView(generics.CreateAPIView):
    """
    Создание помещения(зала) в торговой точке.
    """
    serializer_class = RoomAllFieldSerializer
    permission_classes = (IsSuperuser, )

    def get_queryset(self):
        return Room.objects.all()

    def perform_create(self, serializer):
        if 'pk' in self.kwargs:
            pk = self.kwargs["pk"]
            try:
                serviceplace = ServicePlace.objects.get(id=pk)
            except ServicePlace.DoesNotExist:
                return exceptions.NotFound(_(f'Service place not found.'))
            return serializer.save(aervicePlace=serviceplace)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     print(serializer.data)
    #     if 'pk' in self.kwargs:
    #         pk = self.kwargs["pk"]
    #         serializer.data["servicePlace"] = pk
    #         # try:
    #         #     serviceplace = ServicePlace.objects.get(id=pk)
    #         # except ServicePlace.DoesNotExist:
    #         #     return exceptions.NotFound(_(f'Service place not found.'))
    #         # room = Room.objects.create(servicePlace=serviceplace)
    #         self.perform_create(serializer)
    #         headers = self.get_success_headers(serializer.data)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    #         # return response.Response(data=self.serializer_class(data=room), status=status.HTTP_201_CREATED)


class RoomListView(generics.ListAPIView):
    """
    Список помещений(залов) в определенной торговой точке.
    """
    serializer_class = RoomAllFieldSerializer
    permission_classes = (IsCashier, )

    def get_queryset(self):
        if 'pk' in self.kwargs:
            pk = self.kwargs["pk"]
            try:
                sp = ServicePlace.objects.get(pk=pk)
                return Room.objects.filter(servicePlace=sp)
            except ServicePlace.DoesNotExist:
                raise exceptions.NotFound(_(f'Service place not found.'))


class FranchiseCreateView(generics.CreateAPIView):
    """
    Создание сети/франшизы.
    """
    serializer_class = FranchiseAllFieldsSerializer
    permission_classes = (IsSuperuser, )
    # parser_classes = (parsers.MultiPartParser, )
    queryset = Franchise.objects.all()


class FranchiseListView(generics.ListAPIView):
    """
    Список всех брендов, зарегистрированных в системе.
    """
    serializer_class = FranchiseAllFieldsSerializer
    permission_classes = (IsSuperuser, )
    queryset = Franchise.objects.all()


class ServicePlaceCreateView(generics.CreateAPIView):
    """
    Создание точки обслуживания.
    """
    serializer_class = ServicePlaceRegisterSerializer
    permission_classes = (IsSuperuser, )
    queryset = ServicePlace.objects.all()


class ServicePlaceListView(generics.ListAPIView):
    """
    Список точек обслуживания.
    """
    serializer_class = ServicePlaceRegisterSerializer
    queryset = ServicePlace.objects.all()
    permission_classes = (IsSuperuser, )


class CompanyCreateView(generics.CreateAPIView):
    """
    Создание компании.
    """
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
    permission_classes = (IsSuperuser, )


class CompanyListView(generics.ListAPIView):
    """
    Список сетей.
    """
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
    permission_classes = (IsSuperuser, )


@swagger_auto_schema(method='post', request_body=get_token_shema)
@api_view(["POST"])
def servicePointCreatorView(request):
    """
    Регистрация приложения в торговой точке.
    Приходит логин и пароль заведения + информация устройства, на котором устанавливается терминал.
    Возвращается - уникальный токен для идентификации терминала.
    """
    print("Hello")
    serializer_class = ServicePlaceTerminalRegistrationSerializer(data=request.data)
    print("Serializer getted!")
    if serializer_class.is_valid():
        print("Validated!")
        response_data = serializer_class.create(serializer_class.validated_data)
        return Response(response_data)
    return Response(data=serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)


#TODO дописать права доступа - только директор данного заведения, как разберемся с правами пользователей.
class ServicePlaceTerminalsLoginPasswordView(generics.RetrieveAPIView):
    """
    Просмотреть логин и пароль регистрации терминала.
    """
    serializer_class = ServicePlaceTerminalsLoginPasswordSerializer
    queryset = ServicePlace.objects.all()


