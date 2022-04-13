from datetime import datetime

import jwt
from rest_framework import exceptions, authentication
from django.utils.translation import gettext_lazy as _
from fcmadmin.settings import SECRET_KEY, ALGORITHM, JWT_ACCESS_TTL


class TerminalTokenChecker:
    """
    Вынесем проверку заголовка и токена терминала в отдельный класс, т.к. это будем использовать
    в двух функциях генерации токенов пользователя.
    """
    def check_terminal_token(self, request):
        HTTP_HEADER_ENCODING = 'iso-8859-1'
        if "Device" not in request.headers:
            raise exceptions.AuthenticationFailed(_("Header \'Device\' not found."))
        if not isinstance(request.headers["Device"], str):
            raise exceptions.AuthenticationFailed(_("Header \'Device\' is not string type."))
        terminal_token = request.headers["Device"].encode(HTTP_HEADER_ENCODING)
        try:
            token = terminal_token.decode('utf-8')
        except UnicodeError:
            raise exceptions.AuthenticationFailed(
                'Invalid terminal\'s token header. Token string should not contain invalid characters.'
            )
        data = {"terminalToken": token}
        return data


class AuthTokenChecker:
    """
    Проверка наличия токена пользователя в заголовках.
    """
    authentication_header_prefix = 'Bearer'

    def check_user_token(self, request):
        data = {}
        auth_header = authentication.get_authorization_header(request).split()
        if not auth_header or auth_header[0].lower() != b'bearer':
            return None

        if len(auth_header) == 1:
            raise exceptions.AuthenticationFailed('Invalid token header. No credential provided.')
        elif len(auth_header) > 2:
            raise exceptions.AuthenticationFailed('Invalid token header. Token string should not contain spaces.')
        try:
            userToken = auth_header[1].decode('utf-8')
        except UnicodeError:
            raise exceptions.AuthenticationFailed(
                'Invalid token header. Token string should not contain invalid characters.'
            )
        data["userToken"] = userToken
        return data


class TokenParser:
    """
    Разобрать токен и вернуть полезные данные (payload).
    """
    def parse_token(self, token):
        try:
            payload = jwt.decode(token, key=SECRET_KEY, algorithms=ALGORITHM)
        except jwt.PyJWTError:
            raise exceptions.AuthenticationFailed('Invalid authentication. Could not decode token.')

        if "exp" in payload.keys():
            token_exp = datetime.fromtimestamp(payload['exp'])
            if token_exp < datetime.now():
                raise exceptions.AuthenticationFailed('Token expired.')
        return payload