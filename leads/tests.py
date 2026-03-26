from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Lead
from products.models import Product


class LeadModelTests(TestCase):
    """Test Lead model"""

    def setUp(self):
        self.product = Product.objects.create(
            name='Test Product',
            model='TEST-001',
            description='Test'
        )
        self.lead = Lead.objects.create(
            full_name='John Doe',
            phone='+998901234567',
            product=self.product
        )

    def test_lead_creation(self):
        """Test creating a lead"""
        self.assertEqual(self.lead.full_name, 'John Doe')
        self.assertEqual(self.lead.phone, '+998901234567')
        self.assertEqual(self.lead.product, self.product)

    def test_lead_string_representation(self):
        """Test lead string representation"""
        expected = f'John Doe - +998901234567 ({self.product.name})'
        self.assertEqual(str(self.lead), expected)


class LeadAPITests(APITestCase):
    """Test Lead API endpoints"""

    def setUp(self):
        self.product = Product.objects.create(
            name='Product A',
            model='PROD-A',
            description='Description A'
        )

    def test_create_lead(self):
        """Test creating a lead via API"""
        data = {
            'full_name': 'Jane Doe',
            'phone': '+998901234567',
            'product': self.product.id
        }
        response = self.client.post('/api/leads/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lead.objects.count(), 1)

    def test_list_leads(self):
        """Test listing leads"""
        Lead.objects.create(
            full_name='Test User',
            phone='+998901234567',
            product=self.product
        )
        
        response = self.client.get('/api/leads/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_total_leads_endpoint(self):
        """Test total leads count endpoint"""
        Lead.objects.create(
            full_name='User 1',
            phone='+998901111111',
            product=self.product
        )
        Lead.objects.create(
            full_name='User 2',
            phone='+998902222222',
            product=self.product
        )
        
        response = self.client.get('/api/leads/total_leads/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_leads'], 2)

    def test_leads_by_product(self):
        """Test leads grouped by product"""
        Lead.objects.create(
            full_name='User 1',
            phone='+998901111111',
            product=self.product
        )
        
        response = self.client.get('/api/leads/leads_by_product/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
