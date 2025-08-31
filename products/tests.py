# products/tests.py
from django.test import TestCase
from .models import Product, Category

class ProductModelTest(TestCase):
    def setUp(self):
        """
        Set up non-modified objects used by all test methods.
        """
        self.category = Category.objects.create(name='Shirts', slug='shirts')
        self.product = Product.objects.create(
            category=self.category,
            name='Classic T-Shirt',
            slug='classic-t-shirt',
            price=25.00
        )

    def test_product_str_representation(self):
        """
        Test that the string representation of the Product is its name.
        """
        self.assertEqual(str(self.product), 'Classic T-Shirt')
        print("Completed: test_product_str_representation")

    def test_product_get_absolute_url(self):
        """
        Test that the get_absolute_url method returns the correct URL.
        """
        expected_url = '/products/classic-t-shirt/'
        self.assertEqual(self.product.get_absolute_url(), expected_url)
        print("Completed: test_product_get_absolute_url")

        