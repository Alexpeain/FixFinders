
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom User Model for Fix Finder.
    We inherit from AbstractUser to keep all standard Django auth features
    (username, password, permissions) but allow future customization.
    """
    # We can add global fields here later if needed
    # e.g., is_provider = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username
