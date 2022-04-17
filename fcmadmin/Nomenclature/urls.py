from django.urls.conf import path, include
from .views import MenuCreateView, DishCategoryCreateView
from .views import DishTagsCreateView, DishesCreateView, DishTagsListView
from .views import DishCategoryListView, DishTagsByCategoryIdListView
from .views import DishesFromCategoryWithTagsListSerializer

app_name = "Nomenclature"

menus_patterns = [
    path('create/', MenuCreateView.as_view()),
]

categories_patterns = [
    path('create/', DishCategoryCreateView.as_view()),
    path('all/', DishCategoryListView.as_view()),
    path('<int:pk>/tags/', DishTagsByCategoryIdListView.as_view()),
    path('<int:pk>/dishes/', DishesFromCategoryWithTagsListSerializer.as_view()),
]

dishtags_patterns = [
    path('create/', DishTagsCreateView.as_view()),
    path('all/', DishTagsListView.as_view()),
]

dish_patterns = [
    path('create/', DishesCreateView.as_view()),
]

urlpatterns = (
    path('menus/', include(menus_patterns)),
    path('dishtags/', include(dishtags_patterns)),
    path('dishes/', include(dish_patterns)),
    path('dishcategories/', include(categories_patterns)),
)