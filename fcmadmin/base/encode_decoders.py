from datetime import datetime, timedelta
from django.db.models import Q
from django.contrib.auth import get_user_model

from rest_framework import authentication, exceptions

import jwt

from typing import Optional

from fcmadmin.settings import SECRET_KEY, ALGORITHM, JWT_ACCESS_TTL

User = get_user_model()


class AuthStaff(authentication.BaseAuthentication):
    """
    Аутентификация rfccbhf на сервере с помощью JWT, используемый префикс - Bearer.
    """
    authentication_header_prefix = 'Bearer'
    HTTP_HEADER_ENCODING = 'iso-8859-1'

    def _check_terminal_token(self, token):
        """
        Проверка токена терминала на валидность.
        """
        try:
            token = token.decode('utf-8')
        except UnicodeError:
            raise exceptions.AuthenticationFailed(
                'Invalid terminal\'s token haeder. Token string should not contain invalid characters.'
            )

        return self._authenticate_credentials(token)

    def _authenticate_credentials(self, token):
        """
        Проверка токена на возможность декодирования, срок жизни и наличие юзера.
        """
        try:
            payload = jwt.decode(token, key=SECRET_KEY, algorithms=ALGORITHM)
        except jwt.PyJWTError:
            raise exceptions.AuthenticationFailed('Invalid authentication. Could not decode token.')
        #
        # try:
        #     user = User.objects.get(id=payload['user_id'])
        # except User.DoesNotExist:
        #     raise exceptions.AuthenticationFailed('No user matching this token was found.')
        print(payload)
        return payload

    def get_terminal_token(self, request):
        """
        Получить токен из заголовка.
        """
        # auth = request.META.get('HTTP_AUTHORIZATION', b'')
        if "Device" in request.headers:
            if isinstance(request.headers["Device"], str):
                return self._check_terminal_token(request.headers["Device"].encode(self.HTTP_HEADER_ENCODING))
            else:
                return None
        else:
            return None
