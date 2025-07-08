from django.db import models
from accounts.models import User
from books.models import Book

# Create your models here.
class BookRequest(models.Model):
    """Requests to borrow or swap a book copy"""
    REQUEST_TYPE_CHOICES = [
        ('borrow', 'Borrow'),
        ('swap', 'Swap'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    request_type = models.CharField(max_length=20, choices=REQUEST_TYPE_CHOICES, default='borrow')
    requested_book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='requests_received')
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests_made')
    
    # For swap requests only
    offered_book = models.ForeignKey(
        Book, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='offered_in_swaps'
    )
    
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    response_date = models.DateTimeField(blank=True, null=True)
    
    # Borrow-specific fields
    expected_return_date = models.DateField(blank=True, null=True)
    actual_return_date = models.DateField(blank=True, null=True)
    
    # Notes
    requester_notes = models.TextField(blank=True, null=True)
    owner_notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        if self.request_type == 'borrow':
            return f"{self.requester.username} wants to borrow {self.requested_book.book.title}"
        else:
            return f"{self.requester.username} wants to swap {self.offered_book.book.title if self.offered_book else 'a book'} for {self.requested_book.book.title}"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.request_type == 'swap' and not self.offered_book:
            raise ValidationError("You must specify a book to offer when making a swap request.")
        if self.offered_book and self.offered_book.owner != self.requester:
            raise ValidationError("You can only offer books you own in a swap.")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class ReadingList(models.Model):
    """User's personal reading lists"""
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
        ('friends', 'Friends Only'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reading_lists')
    books = models.ManyToManyField(Book, related_name='reading_lists')
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default='public')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} (by {self.owner.username})"