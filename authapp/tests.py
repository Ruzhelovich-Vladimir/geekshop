from django.conf import settings
from django.http import response
from django.test import TestCase
from django.test.client import Client

from authapp.models import ShopUser


class TestUserAuthTestCase(TestCase):
    username = 'admin'
    email = 'admin@locahost'
    password = 'admin123'

    def setUp(self):
        self.admin = ShopUser.objects.create_superuser(
            self.username, self.email, self.password)
        self.client = Client()

    def test_user_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)
        self.assertNotContains(response, 'Пользователь')

        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/auth/login/')
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(response.context['user'], self.admin)

        response = self.client.get('/')
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertContains(response, 'Пользователь')

    def test_basket_login_redirect(self):

        response = self.client.get('/basket/')
        self.assertEqual(response.url, '/auth/login/?next=/basket/')
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.username, password=self.password)

        response = self.client.get('/basket/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['basket']), [])

    def test_user_register(self):

        response = self.client.get('/auth/register/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['title'], 'регистрация')
        self.assertTrue(response.context['user'].is_anonymous)

        new_user_data = {
            'username': 'test11',
            'first_name': 'test',
            'password1': 'Zaqmko321',
            'password2': 'Zaqmko321',
            'email': 'test@localhost',
            'age': 18
        }

        response = self.client.post('/auth/register/', data=new_user_data)
        self.assertEqual(response.status_code, 302)

        new_user = ShopUser.objects.get(username=new_user_data['username'])
        activation_url = f"{settings.DOMAIN_NAME}/auth/verify/{new_user_data['email']}/{new_user.activation_key}/"

        print(activation_url)
        response = self.client.get(activation_url)
        self.assertEqual(response.status_code, 200)
