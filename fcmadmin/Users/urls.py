from django.urls import path, include
from .views import UserCreateView, user_refresh, user_login, UserUpdatePasswordView
from .views import ProfileDetailView, UserDetailProfile, UserListView

"""
Схема урлов: 
1) Users/ ... - Все урлы, касающиеся работы с пользователями (создать, войти, удалить, забанить и т.д.).
За пользователей отвечает набор 1 уровня users_patterns.
2) Profiles/... - Все, что касается профилей (анкет пользователя).
За профили отвечает набор 1 уровня profiles_patterns
3) Все это включается в общий набор urlpatterns.
Дальнейшая детализация урлов:
4) Регистрация (создание пользователя) - входит в набор (1)
"""

app_name = 'Users'

urlpatterns = []

auth_patterns = [
    path('login/', user_login),
]

users_patterns = [
    path('create/', UserCreateView.as_view()), #Зарегистрировать нового юзера
    path('refresh/', user_refresh), #Обновить токен юзера
    path('auth/', include(auth_patterns)), #авторизовать юзера
    path('password/change', UserUpdatePasswordView.as_view()),
    path('all/', UserListView.as_view())
]

profiles_patterns = [
    path('get/', ProfileDetailView.as_view()),
    path('change/', UserDetailProfile.as_view()),
]

urlpatterns += (
    path('', include(users_patterns)),
    path('profiles/', include(profiles_patterns)),
)
