import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from providers.models import ProviderProfile, Category

User = get_user_model()

class Command(BaseCommand):
    help = 'Generates 200 mock users and provider profiles for Muse and Namkham'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting data generation...")
        
        # Ensure categories exist
        categories = list(Category.objects.filter(id__in=[3, 4, 6]))
        if not categories:
            self.stdout.write(self.style.ERROR("Categories 3, 4, or 6 not found in the database!"))
            return

        townships = ['Muse', 'Namkham']
        statuses = ['approved', 'pending', 'rejected']
        created_count = 0

        for i in range(200):
            username = f"mock_provider_{i}"
            
            # 1. Create the User first
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    password="TestPassword123!",
                    email=f"{username}@fixfinders.test"
                )
                
                # 2. Create the Provider Profile linked to the User
                status = random.choice(statuses)
                ProviderProfile.objects.create(
                    user=user,
                    category=random.choice(categories),
                    township=random.choice(townships),
                    business_name=f"FixFinders Mock Business {i}",
                    phone_number=f"09{random.randint(200000000, 999999999)}",
                    description="Generated mock description for testing in Muse and Namkham.",
                    is_verified=(status == 'approved'),
                    verification_status=status,
                    created_at=timezone.now()
                )
                created_count += 1
                
        self.stdout.write(self.style.SUCCESS(f"Successfully generated {created_count} Users and Provider Profiles!"))