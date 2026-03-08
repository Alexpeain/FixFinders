from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Category, ProviderProfile, Review
import uuid

User = get_user_model()

@admin.register(ProviderProfile)
class ProviderProfileAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'category', 'township', 'phone_number', 'is_verified')
    # Use 'raw_id_fields' if you have thousands of users, but for now this is fine.
    
    # --- MAGIC TRICK: Hide the User field and auto-create it ---
    exclude = ('user',) 

    def save_model(self, request, obj, form, change):
        if not obj.user_id:
            # Create a fake user automatically
            random_suffix = str(uuid.uuid4())[:8]
            username = f"provider_{random_suffix}"
            user = User.objects.create_user(username=username, password='password123')
            obj.user = user
        super().save_model(request, obj, form, change)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('provider', 'reviewer_name', 'rating', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'rating', 'created_at')
    search_fields = ('reviewer_name', 'comment', 'provider__business_name')
    actions = ['approve_reviews']

    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)
    approve_reviews.short_description = "Approve selected reviews"
