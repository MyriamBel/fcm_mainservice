from django.test import TestCase
from ..models import CustomUser, UserAdditionalEmail, Profile
from django.contrib.auth import get_user_model


class SetupTest(TestCase):
    """
    Тестовые кейсы на правильность создания пользователя.
    """
    def setUp(self):
        user = get_user_model()
        superuser = user.objects.create_superuser(email='superuser@mail.com', password='superuser')
        user0 = user.objects.create(email='user@mail.com', password='12345678')
        user1 = user.objects.create(email='user0@mail.com', password='12345678', whoAdded=user0)
        user2 = user.objects.create(email='user1@mail.com', password='12345678', whoAdded=user1)
        user3 = user.objects.create(email='user2@mail.com', password='12345678', whoAdded=superuser)
        user4 = user.objects.create(email='user3@mail.com', password='12345678', whoAdded=superuser)

    def test_users_get_by_name(self):
        user = get_user_model()

        superuser = user.objects.get(is_superuser=True)

        self.assertEqual(superuser.email, "superuser@mail.com")

    def test_get_user(self):
        user = get_user_model()

        some_user = user.objects.get(email="superuser@mail.com")

        self.assertEqual(some_user.__class__, user)

    def test_get_all_users(self):
        user = get_user_model()
        users = user.objects.all()

        count = 0
        for i in users:
            count += 1

        self.assertEqual(count, 6)

