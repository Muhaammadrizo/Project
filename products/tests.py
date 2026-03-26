from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Product
from stats.models import ViewStats


class ProductModelTests(TestCase):
    """Test Product model"""

    def setUp(self):
        self.product = Product.objects.create(
            name='Test Product',
            model='TEST-2024-001',
            description='Test description'
        )

    def test_product_creation(self):
        """Test creating a product"""
        self.assertEqual(self.product.name, 'Test Product')
        self.assertEqual(self.product.model, 'TEST-2024-001')

    def test_product_string_representation(self):
        """Test product string representation"""
        self.assertEqual(
            str(self.product),
            'Test Product (TEST-2024-001)'
        )


class ProductAPITests(APITestCase):
    """Test Product API endpoints"""

    def setUp(self):
        self.product1 = Product.objects.create(
            name='Product 1',
            model='PROD-001',
            description='Description 1'
        )
        self.product2 = Product.objects.create(
            name='Product 2',
            model='PROD-002',
            description='Description 2'
        )

    def test_list_products(self):
        """Test listing products"""
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_retrieve_product(self):
        """Test retrieving product detail"""
        response = self.client.get(f'/api/products/{self.product1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Product 1')

    def test_product_view_tracking(self):
        """Test that viewing product increments view count"""
        response = self.client.get(f'/api/products/{self.product1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if view was tracked
        stats = ViewStats.objects.get(product=self.product1)
        self.assertGreater(stats.views_count, 0)

    def test_search_products(self):
        """Test searching products"""
        response = self.client.get('/api/products/?search=Product 1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_top_viewed(self):
        """Test getting top viewed products"""
        # Track some views
        for _ in range(5):
            self.client.get(f'/api/products/{self.product1.id}/')
        
        response = self.client.get('/api/products/top_viewed/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
