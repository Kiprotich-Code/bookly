from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    """Custom user model extending Django's AbstractUser"""
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    favorite_genres = models.CharField(max_length=100, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    reading_preferences = models.TextField(blank=True, null=True)
    member_since = models.DateTimeField(auto_now_add=True)
    is_profile_complete = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        if not hasattr(self, 'is_profile_complete'):
            self.is_profile_complete = False
        super().save(*args, **kwargs)