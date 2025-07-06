from rest_framework import serializers
from .models import Book, Genre, BookCopy

# Serializers 
class BookCopySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCopy
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    copies = BookCopySerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = '__all__'

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'
