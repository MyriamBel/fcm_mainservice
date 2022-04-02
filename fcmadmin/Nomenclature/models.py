from django.db import models
from django.utils.translation import gettext_lazy as _
from base.services import get_image_upload, get_video_upload, delete_old_file
from django.contrib.auth import get_user_model
from Companies.models import ServicePlace, StoreHouse
from Dictionaries.models import MeasureUnit


User = get_user_model()


class BaseNomenclature(models.Model):
    name = models.CharField(_('name'), max_length=100, null=False, blank=False)
    isActive = models.BooleanField(_('is active'), default=True)
    dateAdded = models.DateTimeField(_('added date'), auto_now_add=True, editable=False)

    class Meta:
        abstract = True


class Menu(BaseNomenclature):
    """
    В разделе можно создавать и настраивать "меню" - готовые наборы блюд на определенный день.
    Например, в столовой "рыбный день" - в четверг, другие блюда не продаются.
    В большом списке блюд неудобно искать рыбу.
    С помощью "меню" можно настроить отображение в четверг только рыбных блюд, все остальные блюда будут скрыты.
    Меню привязаны к заведению/точке обслуживания и их число для заведения неограничено.
    """
    servicePlace = models.ForeignKey(ServicePlace, on_delete=models.CASCADE, null=False, blank=False)
    description = models.CharField(_('description'), max_length=300, null=False, blank=True)

    class Meta:
        verbose_name = _('menu')
        verbose_name_plural = _('menus')

    def __str__(self):
        return _(self.name)


class DishCategory(BaseNomenclature):
    """
    Категория (группа) блюд. Их можно группировать по определенным признакам.
    Например, "Напитки" или "Горячие бутерброды".
    Каждая категория может относиться к некоторому меню, которое привязано к заведению через главное меню.
    А может не относиться к меню, если она, например, в черновике. Тогда она не отображается на терминале.
    Тогда нужно знать, к какому заведению относится эта категория, чтобы отображать в админке только категории,
    созданные для данного заведения.
    """
    servicePlace = models.ForeignKey(ServicePlace, on_delete=models.CASCADE, null=False, blank=False)
    description = models.CharField(_('description'), max_length=300, null=False, blank=True)
    menu = models.ForeignKey(Menu, blank=True, on_delete=models.SET_DEFAULT, default='')
    image = models.ImageField(_('image'), upload_to=get_image_upload, blank=True, null=True)
    # единица измерения, привязанная к категории меню.
    measureUnit = models.ForeignKey(MeasureUnit, on_delete=models.PROTECT, null=False, blank=True)

    class Meta:
        verbose_name = _('dish category')
        verbose_name_plural = _('dishes categories')

    def __str__(self):
        return _(self.name)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.pk:
            this_record = DishCategory.objects.get(pk=self.pk)
            if this_record.image and this_record.image != self.image:
                delete_old_file(this_record.image.path)
        super(DishCategory, self).save()

    def delete(self, using=None, keep_parents=False):
        if self.image:
            delete_old_file(self.image.path)
        super(DishCategory, self).delete()


class DishSubCategory(BaseNomenclature):
    """
    Категория (группа) блюд. Их можно группировать по определенным признакам.
    Например, "Напитки" или "Горячие бутерброды".
    Каждая категория может относиться к некоторому меню, которое привязано к заведению через главное меню.
    А может не относиться к меню, если она, например, в черновике. Тогда она не отображается на терминале.
    Тогда нужно знать, к какому заведению относится эта категория, чтобы отображать в админке только категории,
    созданные для данного заведения.
    """
    servicePlace = models.ForeignKey(ServicePlace, on_delete=models.CASCADE, null=False, blank=False)
    description = models.CharField(_('description'), max_length=300, null=False, blank=True)
    dishCategory = models.ForeignKey(DishCategory, blank=True, on_delete=models.SET_DEFAULT, default='')
    #Категория может вкладываться в другую категорию - образуется иерархия категорий. Например: салаты-постные, без майонеза и т.д.
    # единица измерения, привязанная к категории меню.
    measureUnit = models.ForeignKey(MeasureUnit, on_delete=models.PROTECT, null=False, blank=True)

    class Meta:
        verbose_name = _('dish subcategory')
        verbose_name_plural = _('dishes subcategories')

    def __str__(self):
        return _(self.name)


class Dish(BaseNomenclature):
    """
    Блюдо - некоторый товар, продукт, который будет продаваться на кассовом терминале.
    Для него можно настроить техкарту (рецептуру), цены и себестоимость,
    указать точки продаж (места реализации).
    Блюда в можно группировать по категориям.
    Этот класс описывает непосредственно блюдо.
    Блюдо может относиться к какому-то меню(точнее, к подкатегориям меню) - тогда оно отображается в терминале.
    Блюдо может входить в подкатегорию.
    Блюдо однозначно относится к заведению. Каждое заведение создает свой набор блюд.
    """
    description = models.CharField(_('description'), max_length=300, null=False, blank=True)
    #Единица измерения, в которых измеряется блюдо. Порции, литры, килограммы.
    measureUnit = models.ForeignKey(MeasureUnit, on_delete=models.PROTECT, null=False, blank=True)
    servicePlace = models.ForeignKey(ServicePlace, on_delete=models.CASCADE, null=False, blank=False)
    dishSubCategory = models.ManyToManyField(DishSubCategory)

    class Meta:
        verbose_name = _('dish')
        verbose_name_plural = _('dishes')

    def __str__(self):
        return _(self.name)


"""
----------------------------------------
До этого места модели сверху проверены.
----------------------------------------
"""


class IngredientsCategory(BaseNomenclature):
    """
    Категория (группа) ингредиентов. Их можно группировать по определенным признакам.
    Например, "Молочные продукты" или "Скоропорт".
    Каждая категория может относиться к некоторому складу, которое привязано к заведению через главное меню.
    А может не относиться. Тогда нужно знать, к какому заведению относится эта категория,
    чтобы отображать только категории, созданные для данного заведения.
    """
    servicePlace = models.ForeignKey(ServicePlace, on_delete=models.CASCADE, null=False, blank=False)
    # единица измерения для категории
    measureUnit = models.ForeignKey(MeasureUnit, on_delete=models.PROTECT, null=False, blank=True)
    description = models.CharField(_('description'), max_length=300, null=False, blank=True)
    storeHouse = models.ManyToManyField(StoreHouse, blank=True)
    #Категория может вкладываться в другую категорию - образуется иерархия категорий. Например: скоропорт-молочка, мясо и т.д.
    parentCategory = models.ForeignKey('self', on_delete=models.CASCADE, null=False, blank=True)

    class Meta:
        verbose_name = _('ingredient category')
        verbose_name_plural = _('ingredients categories')

    def __str__(self):
        return _(self.name)


class Ingredients(BaseNomenclature):
    """
    Ингредиент – это базовый тип продукта, который входит в состав других продуктов
    (блюд, полуфабрикатов и модификаторов). Ингредиенты не продаются на кассовом терминале как самостоятельное блюдо и
    недоступны как часть других блюд. Набор ингредиентов в блюде является фиксированной и неизменяемой составляющей.
    """
    description = models.CharField(_('description'), max_length=300, null=False, blank=True)
    measureUnit = models.ForeignKey(MeasureUnit, on_delete=models.PROTECT, null=False, blank=True)
    servicePlace = models.ForeignKey(ServicePlace, on_delete=models.CASCADE, null=False, blank=False)
    ingredientsCategory = models.ManyToManyField(IngredientsCategory)
    storeHouse = models.ManyToManyField(StoreHouse, blank=True)

    class Meta:
        verbose_name = _('ingredient')
        verbose_name_plural = _('ingredients')

    def __str__(self):
        return _(self.name)


class ModifiersCategory(BaseNomenclature):
    """
    Категория (группа) модификаторов. Их можно группировать по определенным признакам.
    Например, "Соусы" или "Способы приготовления", или "Джемы".
    Каждая категория может относиться к некоторому , которое привязано к заведению через главное меню.
    А может не относиться. Тогда нужно знать, к какому заведению относится эта категория,
    чтобы отображать только категории, созданные для данного заведения.
    """
    servicePlace = models.ForeignKey(ServicePlace, on_delete=models.CASCADE, null=False, blank=False)
    description = models.CharField(_('description'), max_length=300, null=False, blank=True)
    #Категория может вкладываться в другую категорию - образуется иерархия категорий. Например: скоропорт-молочка, мясо и т.д.
    parentCategory = models.ForeignKey('self', on_delete=models.CASCADE, null=False, blank=True)
    # единица измерения, привязанная к категории
    measureUnit = models.ForeignKey(MeasureUnit, on_delete=models.PROTECT, null=False, blank=True)

    class Meta:
        verbose_name = _('modifier category')
        verbose_name_plural = _('modifiers categories')

    def __str__(self):
        return _(self.name)


class Modifiers(BaseNomenclature):
    """
    Модификатор – это изменяемая часть продукта, которая входит в состав данного продукта.
    Модификатор - это ингредиент или характеристика продукта, которая может меняться,
    в зависимости от пожеланий заказчика. Например, размер пиццы, объем кофе, топпинг или вид молока, посуда "с собой",
    используемые в приготовлении. Сам по себе отдельно модификатор не продается на кассовом терминале.
    """
    description = models.CharField(_('description'), max_length=300, null=False, blank=True)
    # единица измерения модификатора
    measureUnit = models.ForeignKey(MeasureUnit, on_delete=models.PROTECT, null=False, blank=True)
    servicePlace = models.ForeignKey(ServicePlace, on_delete=models.CASCADE, null=False, blank=False)
    modifiersCategory = models.ManyToManyField(ModifiersCategory)

    class Meta:
        verbose_name = _('modifier')
        verbose_name_plural = _('modifiers')

    def __str__(self):
        return _(self.name)
