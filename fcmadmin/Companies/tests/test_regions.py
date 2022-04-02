from django.test import TestCase
from ..models import Franchise, Company, ServicePlace


class FranchiseTests(TestCase):
    """
    Тесты для модели Franchise.
    """
    def setUp(self):
        Franchise.objects.create(name='Беларусь')
        pl = Country.objects.create(name='Польша')
        ru = Country.objects.create(name='Россия')
        ukr = Country.objects.create(name='Украина')


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
