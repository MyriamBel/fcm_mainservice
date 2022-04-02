import json
from rest_framework import status
from django.test import TestCase, Client
from ..models import Country
from ..serializers import CountryAllFieldsSerializer


# initialize the APIClient app
client = Client()


class GetAllPuppiesTest(TestCase):
    """ Test module for GET all puppies API """
    def setUp(self):
        Country.objects.create(name='Беларусь')
        Country.objects.create(name='Польша')
        Country.objects.create(name='Россия')
        Country.objects.create(name='Украина')

    def test_get_all_puppies(self):
        # get API response
        response = client.get('/ru/api/v1/regions/countries/all/', HTTP_ACCEPT='application/json')
        # get data from db
        countries = Country.objects.all()
        serializer = CountryAllFieldsSerializer(countries, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
