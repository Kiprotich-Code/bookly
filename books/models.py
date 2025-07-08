from django.db import models
from accounts.models import User

# Models 
class Genre(models.Model):
    """Book genres/categories"""
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

class Book(models.Model):
    """Book with ownership and copy information"""
    GENRE_CHOICES = [
        ("Fiction", "Fiction"),
        ("Non-Fiction", "Non-Fiction"),
        ("Science Fiction", "Science Fiction"),
        ("Fantasy", "Fantasy"),
        ("Mystery", "Mystery"),
        ("Thriller", "Thriller"),
        ("Romance", "Romance"),
        ("Biography", "Biography"),
        ("History", "History"),
        ("Self-Help", "Self-Help"),
        ("Literary Fiction", "Literary Fiction"),
        ("Young Adult", "Young Adult"),
        ("Children's", "Children's"),
        ("Poetry", "Poetry"),
        ("Horror", "Horror"),
    ]

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
        ('requested', 'Requested'),
        ('unavailable', 'Unavailable'),
    ]

    # Book information
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES, blank=True, null=True)
    page_count = models.PositiveIntegerField(blank=True, null=True)
    language = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    
    # Copy/ownership information
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_books')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} (Owned by: {self.owner.username})"