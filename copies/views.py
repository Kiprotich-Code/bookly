from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import BookRequest
from .serializers import BookRequestSerializer
from books.models import BookCopy
from django.db.models import Q

# Views 
class BookRequestViewSet(viewsets.ModelViewSet):
    queryset = BookRequest.objects.select_related('requested_book', 'offered_book', 'requester').prefetch_related('requested_book__book', 'offered_book__book')
    serializer_class = BookRequestSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action == 'list':
            if self.request.user.is_anonymous:
                return qs.none()  # Return empty queryset for anonymous users
            return qs.filter(
                Q(requester_id=self.request.user.id) |
                Q(requested_book__owner_id=self.request.user.id)
            )
        return qs

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        obj = self.get_object()
        if obj.requested_book.owner != request.user:
            return Response(
                {"error": "Only the book owner can approve requests"},
                status=status.HTTP_403_FORBIDDEN
            )
        obj.status = 'approved'
        obj.response_date = timezone.now()
        obj.save()

        # update book copy status 
        obj.requested_book.status = 'borrowed' if obj.request_type == 'borrow' else 'unavailable'
        obj.requested_book.save()

        if obj.offered_book:
            obj.offered_book.status = 'unavailable'
            obj.offered_book.save()

        return Response({'status': 'request approved'})
       

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        obj = self.get_object()
        return Response({'status': 'transaction completed'})