from rest_framework import permissions
from base.checkers import TerminalTokenChecker, AuthTokenChecker, TokenParser


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
        return terminalParsedPayload["service_point_id"] == userParsedPayload["servicePlace"]

    # def has_object_permission(self, request, view, obj):
    #     terminalCheckedToken = TerminalTokenChecker()
    #     terminalToken = terminalCheckedToken.check_terminal_token(request)
    #     authCheckedToken = AuthTokenChecker()
    #     authToken = authCheckedToken.check_user_token(request)
    #     print(terminalToken)
    #     print(authToken)
    #     print(request)
    #     print(view)
    #     return False


# class IsServicePointDirector(permissions.IsAuthenticated):
#     def has_object_permission(self, request, view, obj):
#         return request.user ==