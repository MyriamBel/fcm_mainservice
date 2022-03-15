from django.utils.translation import gettext_lazy as _


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


class ToppingItem:
    TOPPING = 'topping'
    SYRUP = 'syrup'
    COFFEE_VARIETY = 'cof_var'
    toppings_choices = [
        (TOPPING, _('topping')),
        (SYRUP, _('syrup')),
        (COFFEE_VARIETY, _('coffee variety')),
    ]
