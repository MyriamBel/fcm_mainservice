from rest_framework import permissions
from base.checkers import TerminalTokenChecker, AuthTokenChecker, TokenParser
from django.contrib.auth import get_user_model
from Employees.models import Cashier

User = get_user_model()


class IsSuperuser(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return request.user.is_superuser is True


#
# class IsOwner(permissions.IsAuthenticated):
#     def has_object_permission(self, request, view, obj):
#         return request.user == obj.user


class IsCashier(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        terminalCheckedToken = TerminalTokenChecker()
        terminalToken = terminalCheckedToken.check_terminal_token(request)
        print(terminalToken)
        authCheckedToken = AuthTokenChecker()
        authToken = authCheckedToken.check_user_token(request)
        print(authToken)
        parsedToken = TokenParser()
        terminalParsedPayload = parsedToken.parse_token(terminalToken["terminalToken"])
        userParsedPayload = parsedToken.parse_token(authToken["userToken"])
        print(request)
        #TODO проверить этот код
        staff = set()
        for child in Cashier.__subclasses__():
            try:
                cashier = child.objects.get(user=userParsedPayload["user_id"])
                staff.add(cashier)
            except child.DoesNotExist:
                pass

        return terminalParsedPayload["service_point_id"] == userParsedPayload["servicePlace"] and len(staff) > 0

# class IsServicePointDirector(permissions.IsAuthenticated):
#     def has_object_permission(self, request, view, obj):
#         return request.user ==
