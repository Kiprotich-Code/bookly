from django.db import models
from books.models import Book
from accounts.models import User

# Create your models here.

class Review(models.Model):
    """Book reviews by users"""
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('book', 'reviewer')
    
    def __str__(self):
        return f"{self.rating} stars for {self.book.title} by {self.reviewer.username}"

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

class Discussion(models.Model):
    """Book discussion threads"""
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='discussions')
    title = models.CharField(max_length=200)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='discussions_started')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_closed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.title} (about {self.book.title})"

class Comment(models.Model):
    """Comments on discussions"""
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Comment by {self.author.username} on {self.discussion.title}"

class Meeting(models.Model):
    """Book club meetings"""
    title = models.CharField(max_length=200)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, blank=True)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_meetings')
    participants = models.ManyToManyField(User, related_name='meetings_attending')
    date_time = models.DateTimeField()
    location = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} on {self.date_time}"