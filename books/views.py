from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from .models import Book, Genre
from .serializers import BookSerializer, GenreSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from books.permissions import IsOwnerOrReadOnly

class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    
    def get_queryset(self):
        """
        Override to filter by owner for 'my-books' and public access for others
        """
        if self.action == 'my_books':
            return Book.objects.filter(owner=self.request.user)
        return Book.objects.all()
    
    def get_permissions(self):
        """
        Set permissions based on action
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'my_books']:
            return [permissions.IsAuthenticated()]
        elif self.action in ['retrieve', 'list']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsOwnerOrReadOnly()]
    
    def perform_create(self, serializer):
        """
        Auto-set owner when creating a book
        """
        serializer.save(owner=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_books(self, request):
        """
        Custom endpoint for getting only the current user's books
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """
        Handle book creation with merged Book/BookCopy logic
        """
        # Check if book exists (by title + author)
        title = request.data.get('title')
        author = request.data.get('author')
        existing_book = Book.objects.filter(title__iexact=title, author__iexact=author).first()
        
        if existing_book:
            # If book exists, check if user already owns it
            if existing_book.owner == request.user:
                return Response(
                    {"detail": "You already own this book."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            # For this implementation, we'll treat each book as unique to owner
            # Alternatively, you could update the existing book here
        
        # Create new book with current user as owner
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
    
    def update(self, request, *args, **kwargs):
        """
        Ensure only owners can update books
        """
        instance = self.get_object()
        if instance.owner != request.user:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """
        Ensure only owners can delete books
        """
        instance = self.get_object()
        if instance.owner != request.user:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)
    


class GenreViewset(viewsets.ModelViewSet):
    """
    Perform CRUD on Genres
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
