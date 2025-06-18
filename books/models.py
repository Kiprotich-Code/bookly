from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User

# Models 
class Genre(models.Model):
    """Book genres/categories"""
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

class Book(models.Model):
    """Book information"""
    title = models.CharField(max_length=200)
    authors = models.CharField(max_length=200)
    genres = models.ManyToManyField(Genre, related_name='books')
    published_date = models.DateField(blank=True, null=True)
    publisher = models.CharField(max_length=100, blank=True, null=True)
    isbn = models.CharField(max_length=20, blank=True, null=True, unique=True)
    page_count = models.PositiveIntegerField(blank=True, null=True)
    language = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    
    def __str__(self):
        return self.title

class BookCopy(models.Model):
    """Physical/digital copies of books owned by users"""
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('like_new', 'Like New'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
    ]
    
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
        ('requested', 'Requested'),
        ('unavailable', 'Unavailable'),
    ]
    
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='copies')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_books')
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='good')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.book.title} (Owned by: {self.owner.username})"

class BorrowRequest(models.Model):
    """Requests to borrow a book copy"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    book_copy = models.ForeignKey(BookCopy, on_delete=models.CASCADE, related_name='borrow_requests')
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrow_requests')
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    response_date = models.DateTimeField(blank=True, null=True)
    expected_return_date = models.DateField(blank=True, null=True)
    actual_return_date = models.DateField(blank=True, null=True)
    lender_notes = models.TextField(blank=True, null=True)
    borrower_notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.borrower.username} wants to borrow {self.book_copy.book.title}"