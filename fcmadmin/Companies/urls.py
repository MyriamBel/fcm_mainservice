from django.urls import path, include
from .views import FranchiseCreateView, FranchiseListView
from .views import servicePointCreatorView
from .views import ServicePlaceCreateView, ServicePlaceListView
from .views import ServicePlaceTerminalsLoginPasswordView
from .views import CompanyCreateView, CompanyListView
from .views import RoomCreateView, RoomListView
from .views import TableCreateView, TableListView

"""
Схема урлов: 

"""

app_name = 'Companies'

franchise_patterns = [
    path('create/', FranchiseCreateView.as_view()),
    path('all/', FranchiseListView.as_view()),
]

terminal_patterns = [
    path('create/', servicePointCreatorView),
]

company_patterns = [
    path('create/', CompanyCreateView.as_view()),
    path('all/', CompanyListView.as_view()),
]

tables_patterns = [
    path('create/', TableCreateView.as_view()),
]

rooms_patterns = [
    path('create/', RoomCreateView.as_view()),
    path('all/', RoomListView.as_view()),
    path('<int:pk>/tables/', TableListView.as_view()),
]

individual_service_place_patterns = [
    path('terminalinfo/', ServicePlaceTerminalsLoginPasswordView.as_view()),
]

service_place_patterns = [
    path('create/', ServicePlaceCreateView.as_view()),
    path('all/', ServicePlaceListView.as_view()),
    path('<int:pk>/', include(individual_service_place_patterns)),
]

urlpatterns = [
    path('franchises/', include(franchise_patterns)),
    path('terminals/', include(terminal_patterns)),
    path('companies/', include(company_patterns)),
    path('places/', include(service_place_patterns)),
    path('rooms/', include(rooms_patterns)),
    path('tables/', include(tables_patterns)),
]