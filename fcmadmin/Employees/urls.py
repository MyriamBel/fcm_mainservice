from django.urls import path, include
from .views import FranchiseFounderCreateView, FranchiseFounderListView
from .views import CompanyFounderListView, CompanyFounderCreateView
from .views import ServicePlaceFoundersListView, ServicePlaceFoundersCreateView
from .views import ServicePlaceBaristaCreateView, ServicePlaceBaristaListView


app_name = 'Employees'

franchisefounders_patterns = [
    path('create/', FranchiseFounderCreateView.as_view()),
    path('all/', FranchiseFounderListView.as_view()),
]

companyfounders_patterns = [
    path('all/', CompanyFounderListView.as_view()),
    path('create/', CompanyFounderCreateView.as_view()),
]

serviceplacefounders_patterns = [
    path('all/', ServicePlaceFoundersListView.as_view()),
    path('create/', ServicePlaceFoundersCreateView.as_view()),
]

serviceplacebarista_patterns = [
    path('all/', ServicePlaceBaristaListView.as_view()),
    path('create/', ServicePlaceBaristaCreateView.as_view()),
]

urlpatterns = [
    path('franchisefounders/', include(franchisefounders_patterns)),
    path('companyfounders/', include(companyfounders_patterns)),
    path('serviceplacefounders/', include(serviceplacefounders_patterns)),
    path('serviceplacebarista/', include(serviceplacebarista_patterns)),
]
