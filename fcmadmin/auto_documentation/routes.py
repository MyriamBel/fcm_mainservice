from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="FCM API",
      default_version='v1',
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
   path(r'swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path(r'redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   path(r'base_auth/', include('rest_framework.urls')),  # базовая аутентификация реста
]

urlpatterns +=[
   path(r'companies/', include('Companies.urls')),
   path(r'users/', include('Users.urls')),
   path(r'regions/', include('Regions.urls')),
   path(r'employees/', include('Employees.urls')),
   path(r'shifts/', include('Shifts.urls')),
]
