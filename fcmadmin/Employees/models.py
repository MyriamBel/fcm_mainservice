from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from Companies.models import Company, Franchise, ServicePlace
from django.core.exceptions import ValidationError
from base.generators import generate_pin

"""
Группы пользователей, которые имеют отношение к тем или иным объектам франшизы(франшиза, сеть, заведение).
Для групп определены разные правила доступа.
Пользователи, входящие в состав основателей франшизы(FranchiseFounders) имеют право на управление своей франшизой.
Пользователи из FranchiseDirector имеют право на управление ограниченной частью функционала, связанного с франшизой
(просмотр отчётов, управление заведениями).
Пользователи из FranchiseMarketer имеют право на управление акциями по всей франшизе.
Пользователи из FranchiseSupervisor имеют право на контроль заведений.
FranchiseAccountant имеют право доступа к финансовой части франшизы(отчёты, установка цен)
FranchiseHR имеют право управления пользователями по всей франшизе(создание аккаунтов сотрудников и тд)
CompanyFounders имеют право на управление своей сетью.
CompanyDirector имеет право управления ограниченной частью функционала всей сети.
CompanySupervisor имеет право контроля информации по своей сети.
Пользователи из CompanyMarketer имеют право на управление акциями по всей сети.
CompanyAccountant имеют право доступа к финансовой части сети(отчёты, установка цен)
CompanyHR имеют право управления пользователями по всей сети(создание аккаунтов сотрудников и тд)
ServicePlaceFounders - управление точкой обслуживания
ServicePlaceDirector - ограниченная часть управления торговой точкой
ServiceAccountant - бухгалтер заведения - финансовые операции по заведения
ServicePlaceAdministrator - администратор заведения - управление персоналом(графики работ и тд)
ServicePlaceCourier - работа с заказами к доставке
ServicePlaceBarista - работа с заказами к доставке(частично) и на месте(создание, внесение позиций, расчёт)
ServicePlaceWaiter - работа с заказами(создание, внесение позиций, расчёт)

!!! Один аккаунт может иметь разные роли!!!
1) FCM администратор создает по заявке пользователя, включает его в FranchiseFounders и создает связанный с ним
    объект франшизы.
2) FCM администратор создает по заявке пользователя CompanyFounders и объект сети.
3) FCM администратор создает по заявке пользователя ServicePlaceFounders и объект торговой точки.
4) 

"""

user = get_user_model()


class BaseStaff(models.Model):
    class Meta:
        abstract = True


class BaseFranchiseStaff(BaseStaff):
    """
    Базовый класс сотрудников франшизы.
    """
    brand = models.ForeignKey(Franchise, on_delete=models.PROTECT, null=False, blank=False)

    class Meta:
        abstract = True

    # def save(self, force_insert=False, force_update=False, using=None,
    #          update_fields=None):
    #     try:
    #         self.full_clean()
    #     except ValidationError:
    #         raise ValidationError(_("This user is already identified as the founder of this franchise."))


class BaseCompanyStaff(BaseStaff):
    """
    Базовый класс сотрудников компании(сети).
    """
    company = models.ForeignKey(Company, on_delete=models.PROTECT, null=False, blank=False)

    class Meta:
        abstract = True


class BaseServicePlaceStaff(BaseStaff):
    """
    Базовый класс сотрудников отдельно взятого заведения.
    """
    servicePlace = models.ForeignKey(ServicePlace, on_delete=models.PROTECT, null=False, blank=False)

    class Meta:
        abstract = True

    # def save(self, *args, **kwargs):
        # self.full_clean()
        # super(BaseServicePlaceStaff, self).save(*args, **kwargs)
        # try:
        #     self.full_clean()
        #     super(BaseServicePlaceStaff, self).save(*args, **kwargs)
        # except ValidationError as e:
        #     print(e.error_dict)
        #     raise ValidationError(_("This user is already identified as the staff of this place."))


class FranchiseFounders(BaseFranchiseStaff):
    """
    Учредители и акционеры франшизы.

    """
    founder = models.ForeignKey(user, on_delete=models.PROTECT, null=False, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['founder', 'brand'], name='FranchiseFounders')
        ]

    def clean(self):
        if FranchiseFounders.objects.filter(brand=self.brand).filter(founder=self.founder).exists():
            raise ValidationError(_('This user is already identified as the founder of this franchise.'))


class FranchiseDirector(BaseFranchiseStaff):
    """
    Руководитель франшизы, региональный директор.
    """
    director = models.ForeignKey(user, on_delete=models.PROTECT, null=False, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['director', 'brand'], name='FranchiseDirector')
        ]


class FranchiseMarketer(BaseFranchiseStaff):
    """
    Маркетолог франшизы.
    """
    marketer = models.ForeignKey(user, on_delete=models.PROTECT, null=False, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['marketer', 'brand'], name='FranchiseMarketer')
        ]


class FranchiseSupervisor(BaseFranchiseStaff):
    """
    Руководитель направления франшизы (продажи/открытие точек)
    """
    supervisor = models.ForeignKey(user, on_delete=models.PROTECT, null=False, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['supervisor', 'brand'], name='FranchiseSupervisor')
        ]


class FranchiseAccountant(BaseFranchiseStaff):
    """
    Бухгалтер сети.
    """
    accountant = models.ForeignKey(user, on_delete=models.PROTECT, null=False, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['accountant', 'brand'], name='FranchiseAccountant')
        ]


class FranchiseHR(BaseFranchiseStaff):
    """
    Кадровик франшизы.
    """
    hr = models.ForeignKey(user, on_delete=models.PROTECT, null=False, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['hr', 'brand'], name='FranchiseHR')
        ]


class CompanyFounders(BaseCompanyStaff):
    """
    Учредители и акционеры сети.
    """
    founder = models.ForeignKey(user, on_delete=models.PROTECT, null=False, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['founder', 'company'], name='CompanyFounders')
        ]


class CompanyDirector(BaseCompanyStaff):
    """
    Руководитель сети.
    """
    director = models.ForeignKey(user, on_delete=models.PROTECT, null=False, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['director', 'company'], name='CompanyDirector')
        ]


class CompanyMarketer(BaseCompanyStaff):
    """
    Маркетолог сети.
    """
    marketer = models.ForeignKey(user, on_delete=models.PROTECT, null=False, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['marketer', 'company'], name='CompanyMarketer')
        ]


class CompanySupervisor(BaseCompanyStaff):
    """
    Руководитель направления в сети (продажи/открытие точек)
    """
    supervisor = models.ForeignKey(user, on_delete=models.PROTECT, null=False, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['supervisor', 'company'], name='CompanySupervisor')
        ]


class CompanyAccountant(BaseCompanyStaff):
    """
    Бухгалтер сети.
    """
    accountant = models.ForeignKey(user, on_delete=models.PROTECT, null=False, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['accountant', 'company'], name='CompanyAccountant')
        ]


class CompanyHR(BaseCompanyStaff):
    """
    Кадровик сети.
    """
    hr = models.ForeignKey(user, on_delete=models.PROTECT, null=False, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['hr', 'company'], name='CompanyHR')
        ]


class ServicePlaceFounders(BaseServicePlaceStaff):
    """
    Учредители и акционеры заведения.
    """
    founder = models.ForeignKey(user, on_delete=models.PROTECT, null=False, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['founder', 'servicePlace'], name='ServicePlaceFounders')
        ]


class ServicePlaceDirector(BaseServicePlaceStaff):
    """
    Руководитель заведения.
    """
    director = models.ForeignKey(user, on_delete=models.PROTECT, null=False, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['director', 'servicePlace'], name='ServicePlaceDirector')
        ]


class ServicePlaceAccountant(BaseServicePlaceStaff):
    """
    Бухгалтер заведения.
    """
    accountant = models.ForeignKey(user, on_delete=models.PROTECT, null=False, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['accountant', 'servicePlace'], name='ServicePlaceAccountant')
        ]


class ServicePlaceAdministrator(BaseServicePlaceStaff):
    """
    Администратор заведения.
    """
    administrator = models.ForeignKey(user, on_delete=models.PROTECT, null=False, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['administrator', 'servicePlace'], name='ServicePlaceAdministrator')
        ]


class ServicePlaceCourier(BaseServicePlaceStaff):
    """
    Курьер.
    """
    courier = models.ForeignKey(user, on_delete=models.PROTECT, null=False, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['courier', 'servicePlace'], name='ServicePlaceCourier')
        ]


class Cashier(BaseServicePlaceStaff):
    """
    Пин-код авторизации на кассовом терминале. У сотрудника может быть пин-код, а может не быть.
    Пин-код состоит из 4 цифр, автоматически генерируемых системой. Как понять, что аккаунту нужно генерировать пин-код?
    При регистрации аккаунта заполняется булево поле "isCashier".
    Каждое заведение имеет свой набор уникальных пин-кодов для входа в терминал.
    1 заведение - несколько пинкодов. Каждый пинкод однозначно идентифицирует сотрудника в отдельно взятом
    заведении. В рамках заведения не может быть совпадающих пин-кодов.
    В рамках множества заведений пин-коды могут совпадать, но только у разных заведений.
    10!/4 = 3628800/4 = 1451520 комбинаций кодов возможно.
    """
    isCashier = models.BooleanField(default=False)
    pin = models.IntegerField(null=True, blank=True, editable=False)

    class Meta:
        abstract = True


class ServicePlaceBarista(Cashier):
    """
    Бариста заведения.
    """
    barista = models.ForeignKey(user, on_delete=models.PROTECT, null=False, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['barista', 'servicePlace'], name='ServicePlaceBarista')
        ]

    def save(self, *args, **kwargs):
        if self.isCashier:
            pin = ''
            obj = ServicePlaceBarista.objects.filter(servicePlace_id=self.servicePlace_id)
            print(obj)
            pins = set()
            if obj:
                for x in obj:
                    pins.add(x.pin)
            while pin == '' or pin in pins:
                pin = generate_pin()
            self.pin = pin
        super(ServicePlaceBarista, self).save(*args, **kwargs)


class ServicePlaceWaiter(Cashier):
    """
    Официант в заведении.
    """
    waiter = models.ForeignKey(user, on_delete=models.PROTECT, null=False, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['waiter', 'servicePlace'], name='ServicePlaceWaiter')
        ]

    # def save(self, force_insert=False, force_update=False, using=None,
    #          update_fields=None, *args, **kwargs):
    #     if self.isCashier is True:
    #         pin = ''
    #         # Строку ниже можно оптимизировать - вместо кучи запросов к бд сделать выборку в set и сверяться с ним.
    #         while pin == '' or ServicePlaceWaiter.objects.filter(servicePlace=self.servicePlace).filter(
    #                 pin=pin).exists():
    #             pin = generate_pin()
    #         self.pin = pin
    #     super(ServicePlaceWaiter, self).save(*args, **kwargs)
