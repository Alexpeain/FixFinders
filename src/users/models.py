
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom User Model for Fix Finder.
    We inherit from AbstractUser to keep all standard Django auth features
    (username, password, permissions) but allow future customization.
    """
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('provider', 'Provider'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
