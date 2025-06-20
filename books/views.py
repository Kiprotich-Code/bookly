<<<<<<< HEAD
=======
from django.shortcuts import render
>>>>>>> 1ca8d3491e7a5bec56398597c69416f09f81d570
from rest_framework import viewsets
from .models import Book, Genre
from .serializers import BookSerializer, GenreSerializer

# Create your views here.
class BookViewset(viewsets.ModelViewSet):
    """
<<<<<<< HEAD
    Performing CRUD on books
=======
    Viewset to perform CRUD on Books
>>>>>>> 1ca8d3491e7a5bec56398597c69416f09f81d570
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class GenreViewset(viewsets.ModelViewSet):
    """
    Perform CRUD on Genres
    """
    queryset = Genre.objects.all()
<<<<<<< HEAD
    serializer_class = GenreSerializer
=======
    serializer_class = GenreSerializer
>>>>>>> 1ca8d3491e7a5bec56398597c69416f09f81d570
