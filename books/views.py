from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from .models import Book, Genre
from .serializers import BookSerializer, GenreSerializer
from rest_framework.response import Response

# Create your views here.
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [ permissions.IsAuthenticated() ]
        return [ permissions.AllowAny() ]

    def create(self, request):
        # Check if book exists (match by title + author to avoid duplicates)
        title = request.data.get('title')
        authors = request.data.get('authors')
        book = Book.objects.filter(title__iexact=title, authors__iexact=authors).first()

        # Create or update Book
        if not book:
            book_serializer = self.get_serializer(data=request.data)
            book_serializer.is_valid(raise_exception=True)
            book = book_serializer.save()
        else:
            book = Book.objects.get(pk=book.id)  # Explicitly fetch to avoid nested serializer issues

        # Create BookCopy for the current user
        book_copy_data = {
            'book': book.id,
            'owner': request.user.id,
            'condition': request.data.get('condition', 'good'),
            'status': 'available',
            'notes': request.data.get('notes', ''),
        }
        return Response(book_serializer.data, status=status.HTTP_201_CREATED)




class GenreViewset(viewsets.ModelViewSet):
    """
    Perform CRUD on Genres
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
