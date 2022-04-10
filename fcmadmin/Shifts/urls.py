from django.urls import path, include
from .views import cashier_authentication, cashier_refresh

app_name = "Shifts"

auth_patterns = [
    path('access/', cashier_authentication),
    path('refresh/', cashier_refresh),
]

urlpatterns = [
    path('tokens/', include(auth_patterns)),
]
