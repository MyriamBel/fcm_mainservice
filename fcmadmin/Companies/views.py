from .serializers import FranchiseAllFieldsSerializer
from django.contrib.auth import get_user_model
from .models import Franchise
from rest_framework import parsers, generics, response, status, exceptions, permissions
from django.utils.translation import gettext_lazy as _
from base.paginators import Standard10ResultsSetPagination
from base.permissions import IsSuperuser


User = get_user_model()


class FranchiseAddView(generics.CreateAPIView):
    """
    Создание сети/франшизы.
    """
    serializer_class = FranchiseAllFieldsSerializer
    permission_classes = (permissions.IsAuthenticated, )
    parser_classes = (parsers.MultiPartParser, )
    queryset = Franchise.objects.all()
