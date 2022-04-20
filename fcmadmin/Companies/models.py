from django.db import models
from django.utils.translation import gettext_lazy as _
from base.services import get_image_upload, get_video_upload, delete_old_file
from base.choices import Shape, TerminalTypes
from django.contrib.auth import get_user_model
from Regions.models import City
# from base import generators
from base.generators import encrypt_string, decrypt_string, generate_hash_string, \
generate_checkoutterminal_login, generate_checkoutterminal_password
from django.core.exceptions import ValidationError
User = get_user_model()
import hashlib


class BaseOrgInfo(models.Model):
    """
    Базовые поля для сущностей, относящихся к точке обслуживания клиентов.
    """
    name = models.CharField(_('name'), max_length=100, unique=True, null=False, blank=False)
    isActive = models.BooleanField(_('is active'), default=True)
    dateAdded = models.DateTimeField(_('added date'), auto_now_add=True, editable=False)

    class Meta:
        abstract = True


class Franchise(BaseOrgInfo):
    """
    Франшиза - некоторая торговая марка, объединяющая в себе несколько разных компаний.
    У франшизы есть один владелец и есть учредитель(-и).
    """

    class Meta:
        verbose_name = _('franchise')
        verbose_name_plural = _('franchise')

    def __str__(self):
        return _(self.name)


class Company(BaseOrgInfo):
    """
    Компания - некоторое юрлицо, которое действует под определенной вывеской(франшизой).
    У компании есть один директор и есть учредитель(-и).
    Организаций у франшизы/сети может быть несколько (например, ООО, продающее алкоголь, и ИП для продажи блюд
    или несколько организаций, объединенных одной торговой маркой).
    Организация обязательно указывается при создании нового склада и добавлении фискального
    регистратора/банковского терминала в систему.
    """
    franchise = models.ForeignKey(Franchise, on_delete=models.PROTECT, blank=False)

    class Meta:
        verbose_name = _('company')
        verbose_name_plural = _('companies')

    def __str__(self):
        return _(self.name)


class ServicePlace(BaseOrgInfo):
    """
    Точка обслуживания(оно же заведение) - место продаж/предоставления услуг, будь то кофейня, бар и т.д.
    У точки обслуживания есть руководитель(директор).
    В заведениях указывается схема столов.
    Каждая точка обслуживания имеет привязанные к ней и только к ней кассовые(и официантские) терминалы.
    Каждый такой терминал может относиться к точке реализации данного заведения.
    Логины для регистрации терминалов уникальны в пределах всей системы и
    генерируются автоматически при создании точки обслуживания.
    Пароль также генерируется автоматически и не может быть изменен пользователем.
    """
    company = models.ForeignKey(Company, on_delete=models.PROTECT, blank=False)
    city = models.ForeignKey(City, on_delete=models.PROTECT, blank=False)
    street = models.CharField(_('street'), max_length=100, null=False, blank=True)
    houseNumber = models.CharField(_('house number'), max_length=10, null=False, blank=True)
    roomNumber = models.CharField(_('number room'), max_length=10, null=False, blank=True)
    latitude = models.DecimalField(_('latitude'), max_digits=10, decimal_places=7, null=True, blank=True)  # долгота
    longitude = models.DecimalField(_('longitude'), max_digits=10, decimal_places=7, null=True, blank=True)  # широта
    noteAddress = models.CharField(_('notes to the address'), max_length=100, null=False, blank=True)
    about = models.CharField(_('about object'), max_length=300, null=False, blank=True)
    loginCheckoutTerminal = models.CharField(
        _('login for checkout terminal registration'), null=False, editable=False, max_length=50,
        unique=True
    )
    passwordCheckoutTerminal = models.CharField(
        _('password for checkout terminal registration'), null=False, max_length=200, editable=False
    )

    class Meta:
        verbose_name = _('service point')
        verbose_name_plural = _('service points')

    def __str__(self):
        return _(self.name)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        """
        salt является случайной последовательностью, добавленной к строке пароля перед использованием
        хеш-функции.
        salt используется для предотвращения перебора по словарю (dictionary attack) и атак радужной
        таблицы (rainbow tables attacks).
        """
        if not self.pk:
            checkoutterminal_login = ''
            # Строку ниже можно оптимизировать - вместо кучи запросов к бд сделать выборку в set и сверяться с ним.
            while checkoutterminal_login == '' or ServicePlace.objects.filter(loginCheckoutTerminal=checkoutterminal_login).exists():
                checkoutterminal_login = generate_checkoutterminal_login()
            self.loginCheckoutTerminal = checkoutterminal_login
            self.passwordCheckoutTerminal = generate_checkoutterminal_password()
            self.passwordCheckoutTerminal = encrypt_string(self.passwordCheckoutTerminal)
        super(ServicePlace, self).save()

    @staticmethod
    def check_password(login, password):
        gettedObject = ServicePlace.objects.get(loginCheckoutTerminal=login)
        return decrypt_string(gettedObject.passwordCheckoutTerminal) == password


class StoreHouse(BaseOrgInfo):
    """
    На складах хранятся остатки продуктов (блюд, полуфабрикатов, ингредиентов, модификаторов) заведения.
    Склады в дальнейшем указываются во всех документах (например, нельзя создать приходную накладную, не указав склад,
    на который поступят продукты из накладной) раздела Склад, по ним строятся отчеты по по продуктам.
    При создании склада обязательно указывается организация, которой этот склад принадлежит.
    """
    description = models.CharField(max_length=300, null=False, blank=True)
    #несколько складов могут относиться к 1 точке обслуживания, при этом склада без точки обслуживания не существует
    servicePlace = models.ForeignKey(ServicePlace, on_delete=models.PROTECT, blank=False)

    class Meta:
        verbose_name = _('storehouse')
        verbose_name_plural = _('storehouse')

    def __str__(self):
        return _(self.name)


class Room(BaseOrgInfo):
    """
    Помещение - обособленная площадь, относящаяся к точке обслуживания, предназначено для размещения посетителей.
    Точка обслуживания может иметь 1 и более помещений, как, например, 1й и 2й этаж или внутреннее
    помещение и терраса.
    """
    servicePlace = models.ForeignKey(ServicePlace, on_delete=models.CASCADE, blank=False)
    shape = models.CharField(_('table shape'), max_length=3, choices=Shape.shape_choices, default=Shape.RECTANGULAR)
    length = models.DecimalField(_("length"), decimal_places=2, max_digits=5, null=True, blank=True)
    width = models.DecimalField(_("width"), decimal_places=2, max_digits=5, null=True, blank=True)

    class Meta:
        verbose_name = _('room')
        verbose_name_plural = _('rooms')

    def __str__(self):
        return _(self.name)


class Table(BaseOrgInfo):
    """
    Стол - относится к некоторому помещению, имеет места для рассадки гостей.
    Столы в системе предназначены для учета гостей и заказов,
    распределения нагрузки между официантами в больших заведениях.
    """
    room = models.ForeignKey(Room, on_delete=models.CASCADE, blank=False)
    shape = models.CharField(_('table shape'), max_length=3, choices=Shape.shape_choices, default=Shape.RECTANGULAR)
    minCapacity = models.IntegerField(_('minimum number of guests'), ) #минимальное число гостей
    maxCapacity = models.IntegerField(_('maximum number of guests')) #максимальное число гостей
    reservable = models.BooleanField(_('reservable'), default=True) #Участвует ли в резервировании
    isBusy = models.BooleanField(_('is busy'), default=False) #Флаг "занят"
    reservationStart = models.DateTimeField(_('datetime of the start of the reservation'), blank=True, null=True) #время начала резервирования
    length = models.DecimalField(_("max length"), decimal_places=2, max_digits=5, null=True, blank=True)
    width = models.DecimalField(_("max width"), decimal_places=2, max_digits=5, null=True, blank=True)

    class Meta:
        verbose_name = _('table')
        verbose_name_plural = _('tables')

    def __str__(self):
        return _(self.name)


class Seat(BaseOrgInfo):
    """
    Место. Каждое место относится к определенному столу и предназначено для контроля количества гостей,
    которое заведение может вместить, учета обслуженных гостей и т.д.
    """
    table = models.ForeignKey(Table, on_delete=models.CASCADE, blank=False)

    class Meta:
        verbose_name = _('seat')
        verbose_name_plural = _('seats')

    def __str__(self):
        return _(self.name)


class CookingPlace(BaseOrgInfo):
    """
    Место приготовления - это кухня заведения (т.е. место, где готовится то или иное блюдо - например,
    бар тоже может быть местом приготовления для кофе или коктейлей).
    В местах приготовления указывается как его название, так и склад,
    которому принадлежит это место и с которого потом будут списываться продукты для блюд,
    готовящихся в месте приготовления. Кроме того, в месте приготовления указывается принтер,
    на котором будут распечатываться "бегунки" на кухню/бар. Место приготовления можно указать для каждого блюда в
    разделе Номенклатура-Блюда, вкладка Продажи.
    """
    servicePlace = models.ForeignKey(ServicePlace, on_delete=models.CASCADE, blank=False)
    # несколько мест реализации относится к нескольким складам
    storeHouse = models.ManyToManyField(StoreHouse, blank=True)

    class Meta:
        verbose_name = _('place of sale')
        verbose_name_plural = _('places of sale')

    def __str__(self):
        return _(self.name)


# class ServicePlaceEmployees(models.Model):
#     user = models.ForeignKey(User, on_delete=models.PROTECT, blank=False)
#     servicePlace = models.ForeignKey(ServicePlace, on_delete=models.PROTECT, blank=False)
#     isActive = models.BooleanField(_('is active'), default=True)
#     dateJoined = models.DateTimeField(_('joining date'), auto_now_add=True, editable=False)
#
#     class Meta:
#         verbose_name = _('employee')
#         verbose_name_plural = _('employees')
#
#     def __str__(self):
#         return '{} - {}'.format(self.servicePlace, self.user)


class Terminal(BaseOrgInfo):
    """
    Кассовый терминал. Кассовый терминал - это некоторый экземпляр кассового приложения, установленный в точке
    реализации в некотором заведении. Каждый кассовый терминал относится только к определенному заведению и
    может относиться к некоторой точке реализации. Это значит, что привязка к заведению обязательна, а к точке
    реализации - необязательна.
    Для регистрации терминалов используем соответствующий логин и пароль из личного кабинета заведения.
    Каждый кассовый терминал имеет информацию об устройстве, на котором он установлен.
    Это включает в себя:
    Производитель устройства
    Модель устройства
    Серийный номер устройства
    Имеи устройства
    """
    servicePlace = models.ForeignKey(ServicePlace, on_delete=models.CASCADE, blank=False)
    # deviceHash = models.BigIntegerField(editable=False)
    deviceManufacturer = models.CharField(_('device manufacturer'), max_length=50, null=False, blank=False)
    deviceModel = models.CharField(_('device model'), max_length=50, null=False, blank=False)
    deviceSerialNumber = models.CharField(_('device serial number'), max_length=250, null=False, blank=False)
    deviceIMEI = models.CharField(_('device IMEI'), max_length=250, null=False, blank=False)
    terminalSubtype = models.CharField(max_length=10, choices=TerminalTypes.types_choices, default=TerminalTypes.CHECKOUT)
    token = models.CharField(_('token'), max_length=250, null=False, blank=True)

    class Meta:
        verbose_name = _('place of sale')
        verbose_name_plural = _('places of sale')

    def __str__(self):
        return _(self.name)

    def __eq__(self, other):
        return (self.deviceIMEI, self.deviceManufacturer, self.deviceSerialNumber, self.deviceModel) == \
               (self.deviceIMEI, self.deviceManufacturer, self.deviceSerialNumber, self.deviceModel)

    def __hash__(self):
        return hashlib.md5(str(self.deviceIMEI).encode() +
                           str(self.deviceManufacturer).encode() +
                           str(self.deviceSerialNumber).encode() +
                           str(self.deviceModel).encode()).hexdigest()
        # return hash(str(self.deviceIMEI)+str(self.deviceManufacturer)+str(self.deviceSerialNumber)+str(self.deviceModel))

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, *args, **kwargs):
        if not self.pk:
            new_name = self.__hash__()
            if not Terminal.objects.filter(name=new_name).exists():
                self.name = new_name

            else:
                raise ValidationError(_("Combination of {}, {}, {}, {} is not unique".format(self.deviceManufacturer,
                                                                                          self.deviceModel,
                                                                                          self.deviceSerialNumber,
                                                                                          self.deviceIMEI)))
        super(Terminal, self).save()


class SalePlace(BaseOrgInfo):
    """
    Место реализации - все точки/сервисы, которые предоставляются из данной точки реализации.
    Это может быть выездная торговля, доставка в номер, бар(как отдельная точка в кафе).
    Место реализации - это точка продаж (им может быть как, например, отдельный этаж ресторана со своей кассой,
    так и киоск "кофе с собой" на улице), к нему привязывается кассовый терминал;
    место реализации отображается в чеках и кассовых сменах этого терминала и отчетах бэк-офиса.
    К месту реализации привязывается схема столов в заведении, настраиваются принтеры для печати пречеков.
    """
    servicePlace = models.ForeignKey(ServicePlace, on_delete=models.CASCADE, blank=False)
    #несколько мест реализации может относиться к нескольким местам приготовления(кухням)
    cookingPlace = models.ManyToManyField(CookingPlace, blank=True)
    checkoutTerminal = models.ForeignKey(Terminal, null=False, blank=True, on_delete=models.PROTECT)

    class Meta:
        verbose_name = _('place of sale')
        verbose_name_plural = _('places of sale')

    def __str__(self):
        return _(self.name)


# class TerminalToken(models.Model):
#     """
#     Объект токена, который привязывается к определенному терминалу.
#     """
#     terminal = models.ForeignKey(Terminal, )