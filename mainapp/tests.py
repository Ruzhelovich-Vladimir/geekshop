from django.http import response
from django.test import TestCase
from django.test.client import Client

from mainapp.models import ProductCategory, Product


class TestMainappTestCase(TestCase):

    def setUp(self):
        category = ProductCategory.objects.create(
            name='Тестовая категория'
        )

        Product.objects.create(
            category=category,
            name='Тестовый продукт №1'
        )

        Product.objects.create(
            category=category,
            name='Тестовый продукт №2'
        )
        self.client = Client()

    def test_mainapp_pages(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)

    def test_mainapp_shop(self):
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)

        # response = self.client.get('/products/category/0/')
        # self.assertEqual(response.status_code, 200)

        for category in ProductCategory.objects.all():
            response = self.client.get(f'/products/category/{category.pk}/')
            self.assertEqual(response.status_code, 200)

        for product in Product.objects.all():
            response = self.client.get(f'/products/product/{product.pk}/')
            self.assertEqual(response.status_code, 200)

    def tearDown(self):
        pass
