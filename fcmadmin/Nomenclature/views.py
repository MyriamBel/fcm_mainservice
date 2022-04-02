from .serializers import DishCategoryNameImageFieldsSerializer
from models import DishCategory, DishSubCategory
from django.contrib.auth import get_user_model
from rest_framework import parsers, generics, response, status, exceptions
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class DishCategoryNameImageFieldsView(generics.ListAPIView):
    """
    Список всех категорий в меню.
    """
    serializer_class = DishCategoryNameImageFieldsSerializer
    queryset = DishCategory.objects.all()

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            # queryset just for schema generation metadata
            return DishCategory.objects.none()
        else:
            if 'pk' in self.kwargs:
                menu_pk = self.kwargs['pk']
                if Chain.objects.filter(pk=chain_pk).exists():
                    if Chain.objects.filter(isActive=True):
                        return EmailChain.objects.filter(chain=self.kwargs['pk'])
                    else:
                        raise exceptions.PermissionDenied(_(f'Chain pk {chain_pk} is not active.'))
                else:
                    raise exceptions.NotFound(_(f'Emails for chain\'s pk {chain_pk} not found.'))