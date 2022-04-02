from django.urls import path, include
from .views import CountryCreateView, CountryRetrieveUpdateDestroyView, CountryListView
from .views import CityCreateView, CityListView, CityRetrieveUpdateDestroyView

"""
Схема урлов:
1) Countries/ ... - Все урлы, касающиеся работы со странами (создать, войти, удалить, забанить и т.д.).
За страны отвечает набор 1 уровня countries_patterns.
2) Cities/... - Все, что касается городов.
За города отвечает набор 1 уровня cities_patterns
3) Все это включается в общий набор urlpatterns.
"""

app_name = 'regions'

urlpatterns = []

countries_patterns = [
    path('create/', CountryCreateView.as_view()),
    path('all/', CountryListView.as_view(), name='all_countries'),
    path('single/<int:pk>/', CountryRetrieveUpdateDestroyView.as_view()),
]

cities_patterns = [
    path('create/', CityCreateView.as_view()),
    path('all/', CityListView.as_view()),
    path('single/<int:pk>/', CityRetrieveUpdateDestroyView.as_view()),
]

urlpatterns += (
    path('countries/', include(countries_patterns)),
    path('cities/', include(cities_patterns)),
)
