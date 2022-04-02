from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Franchise


class SetupTest(TestCase):
    """
    Тестовые кейсы на правильность создания франшизы.
    """
    def setUp(self):
        user = get_user_model()
        user.objects.create_superuser(email='superuser@mail.com', password='superuser')
        user.objects.create(email='user@mail.com', password='12345678')
        Franchise.objects.create(name='FCoffee')
        Franchise.objects.create(name='Coffix')
        Franchise.objects.create(name='CoffeeSound')
        Franchise.objects.create(name='У Макса')
        Franchise.objects.create(name='Кофе с собой')
        Franchise.objects.create(name='Кальянная', isActive="False")

    def test_get_by_name(self):
        franchise = Franchise.objects.get(name="FCoffee")

        self.assertTrue(franchise.__class__, Franchise)
        self.assertTrue(franchise.isActive, True)

    def test_get_all(self):
        franchise = Franchise.objects.all()

        count = 0
        for i in franchise:
            count += 1

        self.assertEqual(count, 6)

