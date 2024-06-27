from django.test import TestCase
from rest_framework.test import APITestCase
from .models import Product, Lead
from django.urls import reverse
from .serializers import ProductSerializer, ContactSerializer
from rest_framework import status
from .models import CustomUser, Contact
from django.test import Client
from django.utils import timezone
        

class ProductViewTests(APITestCase):
    
    def setUp(self):
        # Create some test products
        self.product1 = Product.objects.create(product_name="Product 1", product_price=10.0, description="Description 1")
        self.product2 = Product.objects.create(product_name="Product 2", product_price=20.0, description="Description 2")
        self.product3 = Product.objects.create(product_name="Product 3", product_price=15.0, description="Description 3")
        self.list_url = reverse('product-list')
    
    def test_list_products(self):
        response = self.client.get(self.list_url)
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
    
    def test_create_product(self):
        data = {
            'product_name': 'Product 4',
            'product_price': 30.0,
            'description': 'Description 4'
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 4)
        self.assertEqual(Product.objects.get(product_id=4).product_name, 'Product 4')
    
    
    def test_search_filtering(self):
        response = self.client.get(self.list_url, {'search': 'Product 1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]['product_name'], 'Product 1')
    


class LeadModelTests(TestCase):
    
    def setUp(self):
        self.lead = Lead.objects.create(
            title='Mr.',
            first_name='John',
            last_name='Doe',
            lead_source='Referral',
            job_title='Software Developer',
            phone='1234567890',
            office_email='john.doe@example.com',
            personal_email='john.doe@gmail.com',
            address='123 Main St',
            city='Anytown',
            state='Anystate',
            zip_code='12345',
            country='USA',
            company='Example Inc.',
            lead_rating='Hot',
            description='Test lead',
            lead_owner='Owner Name',
            company_id='12345',
            created_by='Admin',
            modified_by='Admin'
        )

    def test_string_representation(self):
        self.assertEqual(str(self.lead), 'Mr. John Doe')

    def test_created_date_auto_now_add(self):
        self.assertIsNotNone(self.lead.created_date)
        self.assertTrue(isinstance(self.lead.created_date, timezone.datetime))

    def test_modified_date_auto_now(self):
        original_modified_date = self.lead.modified_date
        self.lead.save()
        self.assertEqual(self.lead.created_date.date(), timezone.now().date())
        self.assertEqual(self.lead.created_date.time().replace(microsecond=0), timezone.now().time().replace(microsecond=0))


    def test_lead_creation(self):
        lead = Lead.objects.get(id=self.lead.id)
        self.assertEqual(lead.first_name, 'John')
        self.assertEqual(lead.last_name, 'Doe')
        self.assertEqual(lead.lead_source, 'Referral')



class ContactModelTests(TestCase):
    
    def setUp(self):
        self.contact = Contact.objects.create(
            title='Mr.',
            first_name='John',
            last_name='Doe',
            account_name='Doe Inc.',
            job_title='Manager',
            report_to='CEO',
            description='A test contact.',
            phone_number='1234567890',
            office_email='john.doe@doeinc.com',
            personal_email='john.doe@gmail.com',
            address='123 Main St',
            address2='Suite 100',
            city='Anytown',
            zip_or_post_code='12345',
            region='Anystate',
            country='USA',
            modified_by='Admin'
        )

    def test_string_representation(self):
        self.assertEqual(str(self.contact), 'Mr.')

    def test_created_date_auto_now_add(self):
        self.assertIsNotNone(self.contact.created_date)
        self.assertTrue(isinstance(self.contact.created_date, timezone.datetime))
        self.assertEqual(self.contact.created_date.date(), timezone.now().date())
        self.assertEqual(self.contact.created_date.time().replace(microsecond=0), timezone.now().time().replace(microsecond=0))

    def test_modified_date_auto_now(self):
        original_modified_date = self.contact.modified_date
        self.contact.save()
        self.assertNotEqual(self.contact.modified_date, original_modified_date)

    def test_contact_creation(self):
        contact = Contact.objects.get(id=self.contact.id)
        self.assertEqual(contact.first_name, 'John')
        self.assertEqual(contact.last_name, 'Doe')
        self.assertEqual(contact.account_name, 'Doe Inc.')



class ContactSerializerTests(TestCase):

    def setUp(self):
        self.contact_attributes = {
            'title': 'Mr.',
            'first_name': 'John',
            'last_name': 'Doe',
            'account_name': 'Doe Inc.',
            'job_title': 'Manager',
            'report_to': 'CEO',
            'description': 'A test contact.',
            'phone_number': '1234567890',
            'office_email': 'john.doe@doeinc.com',
            'personal_email': 'john.doe@gmail.com',
            'address': '123 Main St',
            'address2': 'Suite 100',
            'city': 'Anytown',
            'zip_or_post_code': '12345',
            'region': 'Anystate',
            'country': 'USA',
            'modified_by': 'Admin'
        }
        
        self.contact = Contact.objects.create(**self.contact_attributes)
        self.serializer = ContactSerializer(instance=self.contact)
    
    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['id', 'title', 'first_name', 'last_name', 'account_name', 'job_title', 'report_to', 'description', 'phone_number', 'office_email', 'personal_email', 'address', 'address2', 'city', 'zip_or_post_code', 'region', 'country', 'created_date', 'modified_by', 'modified_date', 'remarks'])
    
    def test_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['title'], self.contact.title)
        self.assertEqual(data['first_name'], self.contact.first_name)
        self.assertEqual(data['last_name'], self.contact.last_name)
        self.assertEqual(data['account_name'], self.contact.account_name)
        self.assertEqual(data['job_title'], self.contact.job_title)
        self.assertEqual(data['report_to'], self.contact.report_to)
        self.assertEqual(data['description'], self.contact.description)
        self.assertEqual(data['phone_number'], self.contact.phone_number)
        self.assertEqual(data['office_email'], self.contact.office_email)
        self.assertEqual(data['personal_email'], self.contact.personal_email)
        self.assertEqual(data['address'], self.contact.address)
        self.assertEqual(data['address2'], self.contact.address2)
        self.assertEqual(data['city'], self.contact.city)
        self.assertEqual(data['zip_or_post_code'], self.contact.zip_or_post_code)
        self.assertEqual(data['region'], self.contact.region)
        self.assertEqual(data['country'], self.contact.country)
        self.assertEqual(data['modified_by'], self.contact.modified_by)
       



