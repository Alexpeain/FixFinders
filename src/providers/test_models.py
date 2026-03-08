from django.test import TestCase
from models import Provider
# Create your tests here.

class ProviderTestCase(TestCase):
    def setUp(self):
        Provider.objects.create(user="Provider1", business_name="Business1", phone_number="1234567890", description="Test provider 1", verification_status="approved", is_verified=True)
        
        