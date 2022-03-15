from django.urls import path, include
from .views import FranchiseAddView

"""
Схема урлов: 

"""

app_name = 'Companies'

franchise_patterns = [
    path('create/', FranchiseAddView.as_view()),
]

urlpatterns = [
    path('', include(franchise_patterns)),
]