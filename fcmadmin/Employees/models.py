from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from Companies.models import Company, Franchise, ServicePlace


user = get_user_model()


class BaseStaff(models.Model):
    class Meta:
        abstract = True


class BaseFranchiseStaff(BaseStaff):
    brand = models.ForeignKey(Franchise, on_delete=models.PROTECT, null=False, blank=False)

    class Meta:
        abstract = True


class BaseCompanyStaff(BaseStaff):
    company = models.ForeignKey(Company, on_delete=models.PROTECT, null=False, blank=False)

    class Meta:
        abstract = True


class BaseServicePlaceStaff(BaseStaff):
    servicePlace = models.ForeignKey(ServicePlace, on_delete=models.PROTECT, null=False, blank=False)

    class Meta:
        abstract = True


class FranchiseFounders(BaseFranchiseStaff):
    """
    Учредители и акционеры франшизы.
    """
    founder = models.ForeignKey(user, on_delete=models.PROTECT, null=False, blank=False)


class FranchiseDirector(BaseFranchiseStaff):
    """
    Руководитель франшизы, региональный директор.
    """
    director = models.ForeignKey(user, on_delete=models.PROTECT, null=False, blank=False)


class FranchiseMarketer(BaseFranchiseStaff):
    """
    Маркетолог франшизы.
    """
    marketer = models.ForeignKey(user, on_delete=models.PROTECT, null=False, blank=False)


class FranchiseSupervisor(BaseFranchiseStaff):
    """
    Руководитель направления франшизы (продажи/открытие точек)
    """
    supervisor = models.ForeignKey(user, on_delete=models.PROTECT, null=False, blank=False)


class FranchiseAccountant(BaseFranchiseStaff):
    """
    Бухгалтер сети.
    """
    accountant = models.ForeignKey(user, on_delete=models.PROTECT, null=False, blank=False)


class FranchiseHR(BaseFranchiseStaff):
    """
    Кадровик франшизы.
    """
    hr = models.ForeignKey(user, on_delete=models.PROTECT, null=False, blank=False)


class CompanyFounders(BaseCompanyStaff):
    """
    Учредители и акционеры сети.
    """
    founder = models.ForeignKey(user, on_delete=models.PROTECT, null=False, blank=False)


class CompanyDirector(BaseCompanyStaff):
    """
    Руководитель сети.
    """
    director = models.ForeignKey(user, on_delete=models.PROTECT, null=False, blank=False)


class CompanyMarketer(BaseCompanyStaff):
    """
    Маркетолог сети.
    """
    marketer = models.ForeignKey(user, on_delete=models.PROTECT, null=False, blank=False)


class CompanySupervisor(BaseCompanyStaff):
    """
    Руководитель направления в сети (продажи/открытие точек)
    """
    supervisor = models.ForeignKey(user, on_delete=models.PROTECT, null=False, blank=False)


class CompanyAccountant(BaseCompanyStaff):
    """
    Бухгалтер сети.
    """
    accountant = models.ForeignKey(user, on_delete=models.PROTECT, null=False, blank=False)


class CompanyHR(BaseCompanyStaff):
    """
    Кадровик сети.
    """
    hr = models.ForeignKey(user, on_delete=models.PROTECT, null=False, blank=False)


class ServicePlaceFounders(BaseServicePlaceStaff):
    """
    Учредители и акционеры заведения.
    """
    founder = models.ForeignKey(user, on_delete=models.PROTECT, null=False, blank=False)


class ServicePlaceDirector(BaseServicePlaceStaff):
    """
    Руководитель заведения.
    """
    director = models.ForeignKey(user, on_delete=models.PROTECT, null=False, blank=False)


class ServicePlaceAccountant(BaseServicePlaceStaff):
    """
    Бухгалтер заведения.
    """
    accountant = models.ForeignKey(user, on_delete=models.PROTECT, null=False, blank=False)


class ServicePlaceAdministrator(BaseServicePlaceStaff):
    """
    Администратор заведения.
    """
    administrator = models.ForeignKey(user, on_delete=models.PROTECT, null=False, blank=False)


class ServicePlaceCourier(BaseServicePlaceStaff):
    """
    Курьер.
    """
    courier = models.ForeignKey(user, on_delete=models.PROTECT, null=False, blank=False)


class ServicePlaceBarista(BaseServicePlaceStaff):
    """
    Бариста заведения.
    """
    barista = models.ForeignKey(user, on_delete=models.PROTECT, null=False, blank=False)


class ServicePlaceWaiter(BaseServicePlaceStaff):
    """
    Официант в заведении.
    """
    waiter = models.ForeignKey(user, on_delete=models.PROTECT, null=False, blank=False)