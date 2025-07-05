from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    """Custom user model extending Django's AbstractUser"""
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    favorite_genres = models.JSONField(default=list)  # Changed from CharField to JSONField
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    reading_preferences = models.JSONField(default=list)  # Changed from TextField to JSONField
    member_since = models.DateTimeField(auto_now_add=True)
    is_profile_complete = models.BooleanField(default=False)  # Changed default to False
    
    # New fields for reading statistics and privacy
    reading_goal = models.PositiveIntegerField(default=12)
    books_read = models.PositiveIntegerField(default=0)
    total_swaps = models.PositiveIntegerField(default=0)
    average_rating = models.FloatField(default=0.0)
    privacy_settings = models.JSONField(
        default={
            'show_email': False,
            'show_location': True,
            'show_reading_stats': True
        }
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.username
    
    @property
    def name(self):
        """Alias for username to match frontend expectation"""
        return self.username
    
    def save(self, *args, **kwargs):
        """Set profile complete status based on required fields"""
        required_fields_complete = all([
            self.email,
            self.username,
            self.bio,
            self.location,
            self.favorite_genres
        ])
        self.is_profile_complete = required_fields_complete
        super().save(*args, **kwargs)