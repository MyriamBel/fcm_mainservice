from drf_yasg import openapi

login_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'email': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
    },
    required=['email', 'password', ]
)

token_refresh_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'refreshToken': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
    },
    required=['refreshToken', ]
)