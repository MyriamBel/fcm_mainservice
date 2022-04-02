from django.test import TestCase, Client
from ..models import CustomUser, UserAdditionalEmail, Profile
from django.contrib.auth import get_user_model


class SetupTest(TestCase):
    """ Test module for GET all puppies API """
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

        i = 0
        list_users = []

        while i < 4:
            list_users.append(user.objects.get(email='user'+str(i)+'@mail.com'))
            i += 1
        print(list_users)

