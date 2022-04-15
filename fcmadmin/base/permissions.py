from rest_framework import permissions
from base.checkers import TerminalTokenChecker, AuthTokenChecker, TokenParser
from django.contrib.auth import get_user_model

# from Employees.models import Cashier

User = get_user_model()


class IsSuperuser(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return request.user.is_superuser is True


#
# class IsOwner(permissions.IsAuthenticated):
#     def has_object_permission(self, request, view, obj):
#         return request.user == obj.user


class IsCashier(permissions.IsAuthenticated):
    """
    Пермишен извлекает два токена из запроса, проверяет их валидность и извлекает полезные данные.
    Вернет True, если:
        id заведения правильный(существует и он isActive=True)
        id заведения в токене терминала и в токене сотрудника совпадают
        тип терминала Checkout
        юзер с таким id есть в системе и его статус is_active = True,
        для этого заведения определен такой сотрудник(Cashier)
        статус аккаунта сотрудника isActive = True
    """

    def has_permission(self, request, view):
        # Проверим токен терминала на валидность:
        terminalCheckedToken = TerminalTokenChecker()
        terminalToken = terminalCheckedToken.check_terminal_token(request)
        # Проверим токен пользователя на валидность:
        authCheckedToken = AuthTokenChecker()
        authToken = authCheckedToken.check_user_token(request)
        # Извлечем полезные данные из токенов терминала и пользователя
        parsedToken = TokenParser()
        terminalParsedPayload = parsedToken.parse_token(terminalToken["terminalToken"])
        print(terminalParsedPayload)
        userParsedPayload = parsedToken.parse_token(authToken["userToken"])
        print(userParsedPayload)
        #TODO:
        # Временный костыль, пока тип токена не пропишем в пэйлоад токена юзера системы и токена терминала.
        # if "token_type" not in terminalParsedPayload.keys():
        #     return False
        servicePlace = userParsedPayload["servicePlace"]
        userId = userParsedPayload["user_id"]
        try:
            user = User.objects.get(pk=userId)
        except User.DoesNotExist:
            return False
        staffRole = userParsedPayload["staff_role"]
        staffId = userParsedPayload["staff_id"]
        # Получим объект класса из строки:
        staffClass = getattr(__import__("Employees.models", globals(), locals(), [staffRole], 0), staffRole)
        servicePlaceClass = getattr(__import__("Companies.models", globals(), locals(), ["ServicePlace"],
                                               0), "ServicePlace")
        try:
            cashier = staffClass.objects.get(pk=staffId)
        except staffClass.DoesNotExist:
            return False
        try:
            servicePlaceObject = servicePlaceClass.objects.get(pk=servicePlace)
        except servicePlaceClass.DoesNotExist:
            return False
        print(cashier.user)
        return (servicePlaceObject.isActive is True) & \
               (servicePlace == terminalParsedPayload["service_point_id"]) & \
               (terminalParsedPayload["terminal_type"].lower() == "checkout") & \
               (user.is_active is True) & \
               (cashier.isActive is True) & \
               (cashier.user.pk == userParsedPayload["user_id"])


# class IsServicePointDirector(permissions.IsAuthenticated):
#     def has_object_permission(self, request, view, obj):
#         return request.user ==
