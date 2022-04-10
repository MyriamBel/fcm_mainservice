from django.urls import path, include
from .views import cashier_authentication

app_name = "Shifts"

auth_patterns = [
    path('access/', cashier_authentication),
]

urlpatterns = [
    path('tokens/', include(auth_patterns)),
]
