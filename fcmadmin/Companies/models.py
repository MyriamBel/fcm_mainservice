from django.db import models
from django.utils.translation import gettext_lazy as _
from base.services import get_image_upload, get_video_upload, delete_old_file
from base.choices import Shape
from django.contrib.auth import get_user_model
from Regions.models import City

User = get_user_model()


class Franchise(models.Model):
    """
    Франшиза - некоторая торговая марка, объединяющая в себе несколько разных компаний.
    У франшизы есть один владелец и есть учредитель(-и).
    """
    name = models.CharField(_('name'), max_length=100, unique=True, null=False, blank=False)
    isActive = models.BooleanField(_('is active'), default=True)
    dateJoined = models.DateTimeField(_('joining date'), auto_now_add=True, editable=False)
    franchiseOwner = models.OneToOneField(
        User, on_delete=models.PROTECT, null=False, blank=False
    )
    franchiseFounder = models.ManyToManyField(
        User, blank=True
    )

    class Meta:
        verbose_name = _('franchise')
        verbose_name_plural = _('franchise')

    def __str__(self):
        return _(self.name)


class Company(models.Model):
    """
    Компания - некоторое юрлицо, которое действует под определенной вывеской(франшизой).
    У компании есть один директор и есть учредитель(-и).
    Организаций у франшизы/сети может быть несколько (например, ООО, продающее алкоголь, и ИП для продажи блюд
    или несколько организаций, объединенных одной торговой маркой).
    Организация обязательно указывается при создании нового склада и добавлении фискального
    регистратора/банковского терминала в систему.
    """
    name = models.CharField(_('name'), max_length=100, unique=True, null=False, blank=False)
    franchise = models.ForeignKey(
        Franchise, on_delete=models.PROTECT, null=False, blank=False
    )
    isActive = models.BooleanField(_('is active'), default=True)
    dateJoined = models.DateTimeField(_('joining date'), auto_now_add=True, editable=False)
    companyDirector = models.OneToOneField(User, on_delete=models.PROTECT, null=False, blank=True)
    companyFounder = models.ManyToManyField(User, blank=True)

    class Meta:
        verbose_name = _('company')
        verbose_name_plural = _('companies')

    def __str__(self):
        return _(self.name)


class ServicePlace(models.Model):
    """
    Точка обслуживания(оно же заведение) - место продаж/предоставления услуг, будь то кофейня, бар и т.д.
    У точки обслуживания есть руководитель(директор).
    В заведениях указывается схема столов.
    """
    name = models.CharField(_('name'), max_length=100, null=False, blank=False)
    company = models.ForeignKey(
        Company, on_delete=models.PROTECT, null=False, blank=False
    )
    isActive = models.BooleanField(_('is active'), default=True)
    dateJoined = models.DateTimeField(_('joining date'), auto_now_add=True, editable=False)
    servicePlaceDirector = models.OneToOneField(User, on_delete=models.PROTECT)
    city = models.ForeignKey(City, on_delete=models.PROTECT, null=False, blank=True)
    street = models.CharField(_('street'), max_length=100, null=False, blank=True)
    houseNumber = models.CharField(_('house number'), max_length=10, null=False, blank=True)
    roomNumber = models.CharField(_('number room'), max_length=10, null=False, blank=True)
    latitude = models.DecimalField(_('latitude'), max_digits=10, decimal_places=7, null=False, blank=True)  # долгота
    longitude = models.DecimalField(_('longitude'), max_digits=10, decimal_places=7, null=False, blank=True)  # широта
    noteAddress = models.CharField(_('notes to the address'), max_length=100, null=False, blank=True)
    about = models.CharField(_('about object'), max_length=300, null=False, blank=True)

    class Meta:
        verbose_name = _('service point')
        verbose_name_plural = _('service points')

    def __str__(self):
        return _(self.name)


class StoreHouse(models.Model):
    """
    На складах хранятся остатки продуктов (блюд, полуфабрикатов, ингредиентов, модификаторов) заведения.
    Склады в дальнейшем указываются во всех документах (например, нельзя создать приходную накладную, не указав склад,
    на который поступят продукты из накладной) раздела Склад, по ним строятся отчеты по по продуктам.
    При создании склада обязательно указывается организация, которой этот склад принадлежит.
    """
    name = models.CharField(_('name'), max_length=100, null=False, blank=False)
    isActive = models.BooleanField(_('is active'), default=True)
    dateJoined = models.DateTimeField(_('joining date'), auto_now_add=True, editable=False)
    description = models.CharField(max_length=300, null=False, blank=True)
    #несколько складов могут относиться к 1 точке обслуживания, при этом склада без точки обслуживания не существует
    servicePlace = models.ForeignKey(ServicePlace, on_delete=models.PROTECT, null=False, blank=False)

    class Meta:
        verbose_name = _('storehouse')
        verbose_name_plural = _('storehouse')

    def __str__(self):
        return _(self.name)


class Room(models.Model):
    """
    Помещение - обособленная площадь, относящаяся к точке обслуживания, предназначено для размещения посетителей.
    Точка обслуживания может иметь 1 и более помещений, как, например, кафе.
    """
    name = models.CharField(_('name'), max_length=100, null=False, blank=False)
    servicePlace = models.ForeignKey(ServicePlace, on_delete=models.CASCADE, null=False,
                                     blank=False)
    isActive = models.BooleanField(_('is active'), default=True)
    dateJoined = models.DateTimeField(_('joining date'), auto_now_add=True, editable=False)

    class Meta:
        verbose_name = _('room')
        verbose_name_plural = _('rooms')

    def __str__(self):
        return _(self.name)


class Table(models.Model):
    """
    Стол - относится к некоторому помещению, имеет места для рассадки гостей.
    Столы в системе предназначены для учета гостей и заказов,
    распределения нагрузки между официантами в больших заведениях.
    """
    name = models.CharField(_('name'), max_length=100, null=False, blank=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=False,
                             blank=False)
    isActive = models.BooleanField(_('is active'), default=True)
    dateJoined = models.DateTimeField(_('joining date'), auto_now_add=True, editable=False)
    shape = models.CharField(_('table shape'), max_length=3, choices=Shape.shape_choices, default=Shape.RECTANGULAR)
    minCapacity = models.IntegerField(_('minimum number of guests'), ) #минимальное число гостей
    maxCapacity = models.IntegerField(_('maximum number of guests')) #максимальное число гостей
    reservable = models.BooleanField(_('reservable'), default=True) #Участвует ли в резервировании
    isBusy = models.BooleanField(_('is busy'), default=False) #Флаг "занят"
    reservationStart = models.DateTimeField(_('datetime of the start of the reservation')) #время начала резервирования

    class Meta:
        verbose_name = _('table')
        verbose_name_plural = _('tables')

    def __str__(self):
        return _(self.name)


class Seat(models.Model):
    """
    Место. Каждое место относится к определенному столу и предназначено для контроля количества гостей,
    которое заведение может вместить, учета обслуженных гостей и т.д.
    """
    name = models.CharField(_('name'), max_length=100, null=False, blank=False)
    table = models.ForeignKey(Table, on_delete=models.CASCADE, null=False,
                              blank=False)
    isActive = models.BooleanField(_('is active'), default=True)
    dateJoined = models.DateTimeField(_('joining date'), auto_now_add=True, editable=False)

    class Meta:
        verbose_name = _('seat')
        verbose_name_plural = _('seats')

    def __str__(self):
        return _(self.name)


class CookingPlace(models.Model):
    """
    Место приготовления - это кухня заведения (т.е. место, где готовится то или иное блюдо - например,
    бар тоже может быть местом приготовления для кофе или коктейлей).
    В местах приготовления указывается как его название, так и склад,
    которому принадлежит это место и с которого потом будут списываться продукты для блюд,
    готовящихся в месте приготовления. Кроме того, в месте приготовления указывается принтер,
    на котором будут распечатываться "бегунки" на кухню/бар. Место приготовления можно указать для каждого блюда в
    разделе Номенклатура-Блюда, вкладка Продажи.
    """
    name = models.CharField(_('name'), max_length=100, null=False, blank=False)
    servicePlace = models.ForeignKey(ServicePlace, on_delete=models.CASCADE, null=False,
                                     blank=False)
    isActive = models.BooleanField(_('is active'), default=True)
    dateJoined = models.DateTimeField(_('joining date'), auto_now_add=True, editable=False)
    # несколько мест реализации относится к нескольким складам
    storeHouse = models.ManyToManyField(StoreHouse, blank=True)

    class Meta:
        verbose_name = _('place of sale')
        verbose_name_plural = _('places of sale')

    def __str__(self):
        return _(self.name)


class SalePlace(models.Model):
    """
    Место реализации - все точки/сервисы, которые предоставляются из данной точки реализации.
    Это может быть выездная торговля, доставка в номер, бар(как отдельная точка в кафе).
    Место реализации - это точка продаж (им может быть как, например, отдельный этаж ресторана со своей кассой,
    так и киоск "кофе с собой" на улице), к нему привязывается кассовый терминал;
    место реализации отображается в чеках и кассовых сменах этого терминала и отчетах бэк-офиса.
    К месту реализации привязывается схема столов в заведении, настраиваются принтеры для печати пречеков.
    """
    name = models.CharField(_('name'), max_length=100, null=False, blank=False)
    servicePlace = models.ForeignKey(ServicePlace, on_delete=models.CASCADE, null=False,
                                     blank=False)
    isActive = models.BooleanField(_('is active'), default=True)
    dateJoined = models.DateTimeField(_('joining date'), auto_now_add=True, editable=False)
    #несколько мест реализации может относиться к нескольким местам приготовления(кухням)
    cookingPlace = models.ManyToManyField(CookingPlace, blank=True)

    class Meta:
        verbose_name = _('place of sale')
        verbose_name_plural = _('places of sale')

    def __str__(self):
        return _(self.name)


