from datetime import datetime, timedelta
from django.db.models import Q
from django.contrib.auth import get_user_model, backends

from rest_framework import authentication, exceptions

import jwt

from typing import Optional

from fcmadmin.settings import SECRET_KEY, ALGORITHM, JWT_ACCESS_TTL

User = get_user_model()


class EmailBackend(backends.ModelBackend):
    """
    Custom Backend to perform authentication via email or phone
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            if request.user.email != '':
                username = request.user.email
            else:
                return None
        if password is None:
            return None
        try:
            # Try to fetch the user by searching the username or email field
            user = User.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password) and user.user_can_authenticate(user):
                return user
        except User.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            User().set_password(password)


class AuthBackend(authentication.BaseAuthentication):
    """
    Базовая аутентификация на сервере с помощью JWT, используемый префикс - Bearer
    """
    authentication_header_prefix = 'Bearer'

    def authenticate(self, request, token=None, **kwargs) -> Optional[tuple]:
        """
        Проверяет токен и возвращает его полезные данные, если он прошел проверки
        """
        auth_header = authentication.get_authorization_header(request).split()

        if not auth_header or auth_header[0].lower() != b'bearer':
            return None

        if len(auth_header) == 1:
            raise exceptions.AuthenticationFailed('Invalid token header. No credential provided.')
        elif len(auth_header) > 2:
            raise exceptions.AuthenticationFailed('Invalid token header. Token string should not contain spaces.')

        try:
            token = auth_header[1].decode('utf-8')
        except UnicodeError:
            raise exceptions.AuthenticationFailed(
                'Invalid token header. Token string should not contain invalid characters.'
            )

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, token) -> tuple:
        """
        Проверка токена на возможность декодирования, срок жизни и наличие юзера.
        """
        try:
            payload = jwt.decode(token, key=SECRET_KEY, algorithms=ALGORITHM)
        except jwt.PyJWTError:
            raise exceptions.AuthenticationFailed('Invalid authentication. Could not decode token.')

        token_exp = datetime.fromtimestamp(payload['exp'])
        if token_exp < datetime.now():
            raise exceptions.AuthenticationFailed('Token expired.')

        try:
            user = User.objects.get(id=payload['user_id'])
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No user matching this token was found.')

        return user, None