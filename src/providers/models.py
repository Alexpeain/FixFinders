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
    
    # Verification Status
    VERIFICATION_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    verification_status = models.CharField(
        max_length=10, 
        choices=VERIFICATION_STATUS_CHOICES, 
        default='pending'
    )
    is_verified = models.BooleanField(default=False)
    rejection_reason = models.TextField(blank=True, null=True)

    # Documents
    verification_photo_pink_card = models.ImageField(upload_to='verification_docs/', blank=True, null=True)
    verification_photo_smart_card = models.ImageField(upload_to='verification_docs/', blank=True, null=True)

    # ADD THIS LINE:
    created_at = models.DateTimeField(auto_now_add=True) 

    # --- BADGE PROPERTIES ADDED HERE ---
    @property
    def badge_css_class(self):
        if self.verification_status == 'approved' or self.is_verified:
            return 'bg-success'
        elif self.verification_status == 'rejected':
            return 'bg-danger'
        return 'bg-warning text-dark'

    @property
    def badge_text(self):
        if self.is_verified and self.verification_status != 'approved':
            return 'Verified'
        return self.get_verification_status_display()
    # -----------------------------------

    def __str__(self):
        return f"{self.business_name} ({self.township})"


class Review(models.Model):
    provider = models.ForeignKey(ProviderProfile, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews_given', null=True, blank=True)
    reviewer_name = models.CharField(max_length=100, blank=True, help_text="Fallback name for non-logged-in users")
    
    rating = models.PositiveSmallIntegerField(
        choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')],
        default=5
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Review for {self.provider.business_name} - {self.rating} Stars"
