from rest_framework import serializers
from .models import Book, Genre

# Serializers 
class BookSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'genre', 'page_count', 'language',
            'description', 'cover_image', 'owner', 'owner_username',
            'status', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['owner']  # Owner is set automatically

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'
