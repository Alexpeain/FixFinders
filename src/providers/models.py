from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, default="🔧")
    
    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class ProviderProfile(models.Model):
    # Link to User
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='provider_profile')
    
    # --- THIS IS THE MISSING FIELD ---
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='providers')
    # ---------------------------------

    township = models.CharField(
        max_length=50, 
        choices=[('Muse', 'Muse'), ('Namkham', 'Namkham')],
        default='Muse',
        db_index=True
    )
    
    business_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    
    # Verification
    is_verified = models.BooleanField(default=False)
    verification_photo = models.ImageField(upload_to='private_ids/', blank=True, null=True)

    # ADD THIS LINE:
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.business_name} ({self.township})"
