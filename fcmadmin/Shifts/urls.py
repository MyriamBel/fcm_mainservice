from django.urls import path, include
from .views import cashier_authentication

app_name = "Shifts"

shifts_patterns = [
    path('', cashier_authentication),
]

urlpatterns = [
    path('', include(shifts_patterns)),
]
