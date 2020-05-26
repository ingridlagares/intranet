from django.test import TestCase, Client
from .models import CustomUser


class UserTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='jonas.teixeira',
            first_name='Jonas Teixeira',
            last_name='da Silva',
            email='jonas@gmail.com',
            phone='31972334125',
            profile='PROFESSOR',
            title='prof',
            is_active=True,
            is_admin=False
        )

        self.user.set_password('senhajonas')
        self.user.save()

    def test_incorrect_creds(self):
        client = Client()
        login = client.login(
            username='.',
            password='.'
        )

        self.assertFalse(login)

    def test_login_works(self):
        client = Client()
        login = client.login(
            username='jonas.teixeira',
            password='senhajonas'
        )

        self.assertTrue(login)
