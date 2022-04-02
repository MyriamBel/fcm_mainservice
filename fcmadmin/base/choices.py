from django.utils.translation import gettext_lazy as _


class Shape:
    CIRCLE = 'cir'
    RECTANGULAR = 'rec'
    shape_choices = [
        (CIRCLE, _('circle')),
        (RECTANGULAR, _('rectangular')),
    ]


class Sex:
    MALE = 'm'
    FEMALE = 'f'
    sex_choices = [
        (MALE, _('male')),
        (FEMALE, _('female'))
    ]


class WeekDays:
    MONDAY = 'mon'
    TUESDAY = 'tue'
    WEDNESDAY = 'tue'
    THURSDAY = 'thu'
    FRIDAY = 'fri'
    SATURDAY = 'sat'
    SUNDAY = 'sun'
    weekdays_choices = [
        (MONDAY, _('monday')),
        (TUESDAY, _('tuesday')),
        (WEDNESDAY, _('wednesday')),
        (THURSDAY, _('thursday')),
        (FRIDAY, _('friday')),
        (SATURDAY, _('saturday')),
        (SUNDAY, _('sunday')),
    ]


class TerminalTypes:
    CHECKOUT = 'Checkout'
    WAITER = 'Waiter'
    types_choices = [
        (CHECKOUT, _('Checkout')),
        (WAITER, _('Waiter')),
    ]


# class ToppingItem:
#
#     TOPPING = 'topping'
#     SYRUP = 'syrup'
#     COFFEE_VARIETY = 'cof_var'
#     toppings_choices = [
#         (TOPPING, _('topping')),
#         (SYRUP, _('syrup')),
#         (COFFEE_VARIETY, _('coffee variety')),
#     ]

# class WriteOffType:
#     """
#      Метод списания – этот параметр определяет списание продуктов со склада. Важен для корректного складского учёта.
#     По техкарте – со склада будут списываться продукты, указанные в технологической карте модификатора.
#     Подходит для продуктов, которые готовятся после заказа.
#     По продукту – со склада будет списываться сам модификатор.
#     Подходит для готовых продуктов (например, соус для картофеля фри, который покупается в готовом виде).
#     Сначала по продукту, затем по техкарте – сначала списывается готовый модификатор, когда он заканчивается на складе, списываются продукты, входящие в его техкарту.
#     Подходит для продуктов, которые могут готовиться как заранее, так и после заказа или приготавливаться дополнительно в течение дня в определенном количестве.
#     Не списывать – модификатор не будет списываться со склада.
#     Подходит для продуктов, которые не нуждаются в складском учёте.
#     """
#     FLOWSHEET = 'flow sheet'
#     PRODUCT = 'product'
