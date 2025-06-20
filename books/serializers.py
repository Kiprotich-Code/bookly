from rest_framework import serializers
from .models import Book, Genre

# Serializers 
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name', 'description']

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'authors', 'genres', 'published_date', 'publisher', 'isbn', 'page_count', 'language', 'description', 'cover_image']
