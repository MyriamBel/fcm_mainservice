# from models import DishCategory, DishSubCategory
from django.contrib.auth import get_user_model
from rest_framework import parsers, generics, response, status, exceptions
from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response

from .models import Menu, DishCategory, DishTags, Dish
from .serializers import MenuAllFieldsSerializer, DishCategoryCreateSerializer
from .serializers import DishTagsAllFieldsSerializer, DishesCreateSerializer
from .serializers import DishCategoryImgNameFieldsSerializer, DishTagsIdNameSerializer
from .serializers import DishNamePriceWithTotalSerializer

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
    serializer_class = DishTagsAllFieldsSerializer
    queryset = DishTags.objects.all()
    permission_classes = (IsSuperuser, )


class DishTagsListView(generics.ListAPIView):
    """
    Список тегов для блюд.
    """
    serializer_class = DishTagsAllFieldsSerializer
    queryset = DishTags.objects.all()
    permission_classes = (IsCashier, )


class DishTagsByCategoryIdListView(generics.ListAPIView):
    """
    Список тегов какого-либо пункта меню.
    """
    serializer_class = DishTagsIdNameSerializer
    permission_classes = (IsCashier, )

    def get_queryset(self):
        """
        Получить список тегов, относящихся к пункту меню.
        Выбираются все активные блюда данного пункта меню(категории), из них выбираются теги.
        """
        if getattr(self, 'swagger_fake_view', False):
            # queryset just for schema generation metadata
            return DishTags.objects.none()
        else:
            if 'pk' in self.kwargs:
                dishcategory = self.kwargs['pk']
                try:
                    category = DishCategory.objects.get(pk=dishcategory)
                except DishCategory.DoesNotExist:
                    raise exceptions.NotFound(_(f'Dish category not found.'))
                if category.isActive is not True:
                    raise exceptions.PermissionDenied(_('Dish category is not active.'))
                list_tags = DishTags.objects.exclude(isActive=False).exclude(dish__isActive=False).\
                    filter(dish__dishCategory=category)
                set_tags = set()
                for i in list_tags:
                    set_tags.add(i)
                return set_tags


class DishesCreateView(generics.CreateAPIView):
    """
    Создание блюд.
    """
    serializer_class = DishesCreateSerializer
    queryset = Dish.objects.all()
    permission_classes = (IsSuperuser, )


class DishesFromCategoryWithTagsListSerializer(generics.ListAPIView):
    """
    Вывод списка блюд, относящихся к определенному пункту меню и имеющих определенный тег.
    """
    serializer_class = DishNamePriceWithTotalSerializer
    permission_classes = (IsCashier, )

    def get_queryset(self):
        if 'pk' in self.kwargs:
            dishcategory = self.kwargs['pk']
            query_params = self.request.query_params
            data = Dish.objects.exclude(isActive=False).exclude(dishTag__isActive=False)
            if "tag" in query_params.keys():
                tag = query_params["tag"]
                return data.filter(dishTag=tag).filter(dishCategory=dishcategory)
            return data.filter(dishCategory=dishcategory)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        count = queryset.count()
        return Response({"count": count, "data": serializer.data})


class DishCategoryListView(generics.ListAPIView):
    """
    Список всех категорий меню.
    """

    serializer_class = DishCategoryImgNameFieldsSerializer
    queryset = DishCategory.objects.all()
    permission_classes = (IsCashier, )

    # def get(self, request, *args, **kwargs):
    #     otv = self.check_permissions(request)
    #     print(self.request)
    #     print(self.permissions)
    #     return Response({"otv": otv})

    # def check_permissions(self, request):
        # from rest_framework import permissions

    #     for permission in self.get_permissions():
    #         print(permission)
    #         if not permission.has_permission(request, self):
    #             self.permission_denied(request, message=getattr(permission, 'message', None),
    #                                    code=getattr(permission, 'code', None))

