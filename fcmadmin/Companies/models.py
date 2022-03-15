from django.db import models
from django.utils.translation import gettext_lazy as _
from base.services import get_image_upload, get_video_upload, delete_old_file
from django.contrib.auth import get_user_model


User = get_user_model()

User = get_user_model()


class Franchise(models.Model):
    name = models.CharField(_('name'), max_length=100, unique=True, null=False, blank=False)
    isActive = models.BooleanField(_('is active'), default=False)
    dateJoined = models.DateTimeField(_('joining date'), auto_now_add=True, editable=False)
    franchiseOwner = models.OneToOneField(User, related_name='franchise', on_delete=models.PROTECT)

    class Meta:
        verbose_name = _('franchise')
        verbose_name_plural = _('franchise')

    def __str__(self):
        return _(self.name)


# class Chain(models.Model):
#     name = models.CharField(_('name'), max_length=100, unique=True, null=False, blank=False)
#     isActive = models.BooleanField(_('is active'), default=False)
#     dateJoined = models.DateTimeField(_('joining date'), auto_now_add=True, editable=False)
#     logo = models.ImageField(_('logo'), upload_to=get_image_upload, null=True, blank=True)
#     # city = models.ForeignKey(City, related_name='retailOfficeCity', null=False, blank=False,
#     #                          on_delete=models.PROTECT)
#     # street = models.CharField(_('street'), max_length=100, null=False, blank=True)
#     # houseNumber = models.CharField(_('house number'), max_length=10, null=False, blank=True)
#     # roomNumber = models.CharField(_('number room'), max_length=10, null=False, blank=True)
#     # latitude = models.CharField(_('latitude'), max_length=10, null=False, blank=True)  # долгота
#     # longitude = models.CharField(_('longitude'), max_length=10, null=False, blank=True)  # широта
#     head = models.ManyToManyField(User, related_name='chains')
#
#     class Meta:
#         verbose_name = _('retail chain')
#         verbose_name_plural = _('retail chains')
#
#     def __str__(self):
#         return _(self.name)
#
#     def save(self, force_insert=False, force_update=False, using=None,
#              update_fields=None):
#         if self.pk:
#             this_record = Chain.objects.get(pk=self.pk)
#             if this_record.logo and this_record.logo != self.logo:
#                 delete_old_file(this_record.logo.path)
#         super(Chain, self).save()
#
#     def delete(self, using=None, keep_parents=False):
#         if self.logo:
#             delete_old_file(self.logo.path)
#         super(Chain, self).delete()

#
# class CompanyAccount(models.Model):
#     manager = models.ForeignKey(User, on_delete=models.PROTECT, null=False, blank=False, related_name='stores')

