import jwt
from drf_yasg.utils import swagger_auto_schema
from django.http.response import HttpResponse
from rest_framework import exceptions, status
from django.utils.translation import gettext_lazy as _
from rest_framework.decorators import api_view
from .serializers import StaffDeviceLoginSerializer, StaffDeviceRefreshSerializer
from rest_framework.response import Response
# from .api_shemas import login_schema, token_refresh_schema
from base.checkers import TerminalTokenChecker


# class TerminalTokenChecker:
#     """
#     Вынесем проверку заголовка и токена терминала в отдельный класс, т.к. это будем использовать
#     в двух функциях генерации токенов пользователя.
#     """
#     def check_terminal_token(self, request):
#         HTTP_HEADER_ENCODING = 'iso-8859-1'
#         if "Device" not in request.headers:
#             raise exceptions.AuthenticationFailed(_("Header \'Device\' not found."))
#         if not isinstance(request.headers["Device"], str):
#             raise exceptions.AuthenticationFailed(_("Header \'Device\' is not string type."))
#         terminal_token = request.headers["Device"].encode(HTTP_HEADER_ENCODING)
#         try:
#             token = terminal_token.decode('utf-8')
#         except UnicodeError:
#             raise exceptions.AuthenticationFailed(
#                 'Invalid terminal\'s token header. Token string should not contain invalid characters.'
#             )
#         data = request.data
#         data["terminalToken"] = token
#         return data

# @swagger_auto_schema(method='post', request_body=login_schema)
@api_view(["POST"])
def cashier_authentication(request):
    """
    Авторизация кассира для работы на терминале. Сначала проверим наличие нужного заголовка в запросе.
    Если он есть, то проверим наличие пинкода в теле запроса. Если он тоже есть, то передаем данные в сериализатор.
    Если что-то не так, возвращаем ошибку.
    """
    checker = TerminalTokenChecker()
    request.data["terminalToken"] = checker.check_terminal_token(request)["terminalToken"]
    serializer = StaffDeviceLoginSerializer(data=request.data)
    if serializer.is_valid():
        response_data = serializer.save()
        return Response(response_data)
    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def cashier_refresh(request):
    """
    Рефреш токена кассира терминала. Сначала проверяем наличие нужного заголовка 'Device'.
    Если он есть, разберем рефреш токен и сгенерируем новую пару токенов, если он валидный.
    Все ошибки возвращают соответствующее исключение.
    """
    checker = TerminalTokenChecker()
    data = checker.check_terminal_token(request)
    serializer = StaffDeviceRefreshSerializer(data=data)
    if serializer.is_valid():
        response_data = serializer.save()
        return Response(response_data)
    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)