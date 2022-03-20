from django.db import models
from django.utils.translation import gettext_lazy as _
from Companies.models import ServicePlace


# class NomenclatureCatalog(models.Model):
#     """
#     Каталог справочников. Каждый каталог привязан к своей точке обслуживания.
#     Каталог справочников определяет, к какой точке обслуживания относится тот или иной справочник.
#     Это класс-посредник, он явно нигде не фигурирует и нужен лишь для изолирования справочников друг от друга
#     по признаку принадлежности к той или иной точке обслуживания.
#     """
#     servicePlace = models.ForeignKey(ServicePlace, on_delete=models.CASCADE, null=False, blank=False)
#


class DishTag(models.Model):
    """
    Тэг - это специальная метка, которая объединяет несколько разных блюд из разных групп (папок).
    Например, мы можем отметить тэгом "Маржинальные" все блюда с высокой наценкой,
    и смотреть отчет с такими блюдами, сгрупированными в один блок
    или добавить в инвентаризацию все скоропортящиеся продукты по тэгу "Скоропортящиеся" в один клик.
    """
    name = models.CharField(_('name'), max_length=50, null=False, blank=False)
    active = models.BooleanField(_('deleted'), default=True)
    servicePlace = models.ForeignKey(ServicePlace, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        verbose_name = _('tag')
        verbose_name_plural = _('tags')

    def __str__(self):
        return _(self.name)


class MeasureUnit(models.Model):
    """
    Справочник единиц измерения.
    Здесь можно настроить единицы измерения (килограммы, граммы, литры и т.д.),
    которые будут использоваться в заведении для всех продуктов (блюд, модификаторов, полуфабрикатов, ингредиентов).
    По умолчанию доступны штуки, литры, килограммы, порции;
    при этом можно добавить любую единицу измерения - миллилитры, граммы и т.д
    """
    shortName = models.CharField(_('name'), max_length=10, null=False, blank=False)
    fullName = models.CharField(_('full name'), max_length=50, null=False, blank=False)
    active = models.BooleanField(_('deleted'), default=True)
    servicePlace = models.ForeignKey(ServicePlace, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        verbose_name = _('measure unit')
        verbose_name_plural = _('measure units')

    def __str__(self):
        return _(self.name)


class PackingUnits(models.Model):
    """
        Справочник фасовок.
        Фасовками удобно приходовать на склад ингредиенты, которые поступают в виде упаковок,
        например, рис в пачках 350 г, молоко в бутылках 950 мл. и т.д.
        Например, поступила приходная накладная на 13 пачек риса.
        В одной пачке 350 г (0,35 кг) риса.
        Без фасовок пришлось бы вручную умножать 13 пачек * 0,35 кг (4.55 кг) и указывать полученные кг вручную.
        Фасовкой можно занести в систему пачки по 0,35 кг и приходовать в этих пачках,
        а пересчет в кг выполнит сама система.
        Для одного и того же ингредиента может быть много фасовок (например, рис по 350 г, 500 г).
        """
    name = models.CharField(_('name'), max_length=50, null=False, blank=False)
    # parent ratio - соотношение к родительской единице измерения. Например, для пачек риса это 0,35*1кг
    parentRatio = models.DecimalField(_('parent ratio'), null=False, blank=False, decimal_places=3, max_digits=5)
    active = models.BooleanField(_('deleted'), default=True)
    # родительская единица измерения - та, соотношение к которой вычисляем.
    parentUnit = models.ForeignKey(
        MeasureUnit, on_delete=models.PROTECT, related_name='measureUnit', null=False, blank=False
    )
    servicePlace = models.ForeignKey(ServicePlace, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        verbose_name = _('measure unit')
        verbose_name_plural = _('measure units')

    def __str__(self):
        return _(self.name)
