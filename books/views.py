from django.shortcuts import render
from rest_framework import viewsets
from .models import Book, Genre
from .serializers import BookSerializer, GenreSerializer

# Create your views here.
class BookViewset(viewsets.ModelViewSet):
    """
    Performing CRUD on books
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class GenreViewset(viewsets.ModelViewSet):
    """
    Perform CRUD on Genres
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
