from django.urls import path, include
from .views import FranchiseAddView
from .views import servicePointCreatorView
from .views import ServicePlaceCreateView, CompanyCreateView

"""
Схема урлов: 

"""

app_name = 'Companies'

franchise_patterns = [
    path('create/', FranchiseAddView.as_view()),
]
terminal_patterns = [
    path('create/', servicePointCreatorView),
]
company_patterns = [
    path('create/', CompanyCreateView.as_view()),
]
service_place_patterns = [
    path('create/', ServicePlaceCreateView.as_view()),
]

urlpatterns = [
    path('franchises/', include(franchise_patterns)),
    path('terminals/', include(terminal_patterns)),
    path('companies/', include(company_patterns)),
    path('service_places/', include(service_place_patterns)),
]