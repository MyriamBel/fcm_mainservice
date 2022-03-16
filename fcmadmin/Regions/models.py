from django.db import models
from django.utils.translation import gettext_lazy as _


class Country(models.Model):
    name = models.CharField(_('name'), max_length=50, unique=True, null=False, blank=False)

    class Meta:
        verbose_name = _('country')
        verbose_name_plural = _('countries')

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(_('name'), unique=True, max_length=50, null=False, blank=False)
    countryId = models.ForeignKey(Country, on_delete=models.PROTECT, related_name='cities', null=False, blank=False)

    class Meta:
        verbose_name = _('city')
        verbose_name_plural = _('cities')

    def __str__(self):
        return _(self.name)
