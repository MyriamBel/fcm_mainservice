# import unittest
#
#
# class TestStringMethods(unittest.TestCase):
#
#     def test_upper(self):
#         # assertEqual() для проверки ожидаемого результата
#         self.assertEqual('foo'.upper(), 'FOO')
#
#     def test_isupper(self):
#         # assertTrue() или assertFalse() для проверки услови
#         self.assertTrue('FOO'.isupper())
#         self.assertFalse('Foo'.isupper())
#
#     def test_split(self):
#         # assertRaises() для проверки, что метод порождает исключение
#         s = 'hello world'
#         self.assertEqual(s.split(), ['hello', 'world'])
#         # Проверим, что s.split не работает, если разделитель - не строка
#         with self.assertRaises(TypeError):
#             s.split(2)
#
#
# if __name__ == '__main__':
#     unittest.main()

from django.test import TestCase
from ..models import City, Country


class RegionsTests(TestCase):
    """ Test module for Puppy model """
    def setUp(self):
        blr = Country.objects.create(name='Беларусь')
        pl = Country.objects.create(name='Польша')
        ru = Country.objects.create(name='Россия')
        ukr = Country.objects.create(name='Украина')

        City.objects.create(name="Минск", countryId=blr)
        City.objects.create(name="Варшава", countryId=pl)
        City.objects.create(name="Киев", countryId=ukr)
        City.objects.create(name="Воронеж", countryId=ru)

    def test_city_get_by_name(self):
        city_blr = City.objects.get(name="Минск")
        self.assertEqual(city_blr.__str__(), "Минск")
        country_blr = Country.objects.get(pk=city_blr.countryId.pk)
        print(city_blr.countryId.pk)
        print(country_blr)

    def test_country_get(self):
        country_blr = Country.objects.get(name='Беларусь')
        country_ru = Country.objects.get(name='Россия')
        country_ukr = Country.objects.get(name='Украина')
        country_pl = Country.objects.get(name='Польша')

        self.assertEqual(country_blr.__str__(), "Беларусь")
        self.assertEqual(country_ru.__str__(), "Россия")
        self.assertEqual(country_ukr.__str__(), "Украина")
        self.assertEqual(country_pl.__str__(), "Польша")
