# from models import DishCategory, DishSubCategory
from django.contrib.auth import get_user_model
from rest_framework import parsers, generics, response, status, exceptions
from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response

from .models import Menu, DishCategory, DishTags, Dish
from .serializers import MenuAllFieldsSerializer, DishCategoryCreateSerializer
from .serializers import DishTagsCreateSerializer, DishesCreateSerializer
from .serializers import DishCategoryImgNameFieldsSerializer
from base.permissions import IsSuperuser, IsCashier

User = get_user_model()


# class DishCategoryNameImageFieldsView(generics.ListAPIView):
#     """
#     Список всех категорий в меню.
#     """
#     serializer_class = DishCategoryNameImageFieldsSerializer
#     queryset = DishCategory.objects.all()
#
#     def get_queryset(self):
#         if getattr(self, 'swagger_fake_view', False):
#             # queryset just for schema generation metadata
#             return DishCategory.objects.none()
#         else:
#             if 'pk' in self.kwargs:
#                 menu_pk = self.kwargs['pk']
#                 if Chain.objects.filter(pk=chain_pk).exists():
#                     if Chain.objects.filter(isActive=True):
#                         return EmailChain.objects.filter(chain=self.kwargs['pk'])
#                     else:
#                         raise exceptions.PermissionDenied(_(f'Chain pk {chain_pk} is not active.'))
#                 else:
#                     raise exceptions.NotFound(_(f'Emails for chain\'s pk {chain_pk} not found.'))


class MenuCreateView(generics.CreateAPIView):
    """
    Создание меню для определенного заведения.
    На входе - информацию о меню в теле запроса.
    """
    serializer_class = MenuAllFieldsSerializer
    queryset = Menu.objects.all()
    permission_classes = (IsSuperuser, )


class DishCategoryCreateView(generics.CreateAPIView):
    """
    Создание категории блюд.
    """
    serializer_class = DishCategoryCreateSerializer
    queryset = DishCategory.objects.all()
    permission_classes = (IsSuperuser, )


class DishTagsCreateView(generics.CreateAPIView):
    """
    Создание тегов для блюд.
    """
    serializer_class = DishTagsCreateSerializer
    queryset = DishTags.objects.all()
    permission_classes = (IsSuperuser, )


class DishesCreateView(generics.CreateAPIView):
    """
    Создание блюд.
    """
    serializer_class = DishesCreateSerializer
    queryset = Dish.objects.all()
    permission_classes = (IsSuperuser, )


class DishCategoryListView(generics.ListAPIView):
    """
    Список всех категорий меню.
    """
    from rest_framework import permissions

    serializer_class = DishCategoryImgNameFieldsSerializer
    queryset = DishCategory.objects.all()
    permission_classes = (IsCashier, )

    # def get(self, request, *args, **kwargs):
    #     otv = self.check_permissions(request)
    #     print(self.request)
    #     print(self.permissions)
    #     return Response({"otv": otv})

    # def check_permissions(self, request):
    #     for permission in self.get_permissions():
    #         print(permission)
    #         if not permission.has_permission(request, self):
    #             self.permission_denied(request, message=getattr(permission, 'message', None),
    #                                    code=getattr(permission, 'code', None))

