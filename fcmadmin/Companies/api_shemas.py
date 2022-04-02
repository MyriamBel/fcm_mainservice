from drf_yasg import openapi
from base.choices import TerminalTypes

get_token_shema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'loginCheckoutTerminal': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        'passwordCheckoutTerminal': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        'deviceManufacturer': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        'deviceModel': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        'deviceSerialNumber': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        'deviceIMEI': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        'terminalSubtype': openapi.Schema(type=openapi.TYPE_ARRAY, description='choice', items=TerminalTypes.types_choices),
    },
    required=['loginCheckoutTerminal', 'passwordCheckoutTerminal', 'deviceManufacturer', 'deviceModel',
              'deviceSerialNumber', 'deviceIMEI', 'terminalSubtype']
)