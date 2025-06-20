from rest_framework import serializers
from .models import BookRequest
from books.models import BookCopy
from accounts.models import User


# serializers 
class BookCopyMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCopy
        fields = ['id', 'condition', 'status']

        def to_representation(self, instance):
            data = super().to_representation(instance)
            data['book_title'] = instance.book.title
            data['book_cover'] = instance.book.cover_image.url if instance.book.cover_image else None
            return data
        

class BookRequestSerializer(serializers.ModelSerializer):
    requested_book = BookCopyMinimalSerializer(read_only=True)
    requested_book_id = serializers.PrimaryKeyRelatedField(
        queryset=BookCopy.objects.filter(status='available'),
        write_only=True,
        source='requested_book'
    )

    offered_book = BookCopyMinimalSerializer(read_only=True, required=False)
    offered_book_id = serializers.PrimaryKeyRelatedField(
        queryset=BookCopy.objects.all(),
        write_only=True,
        required=False,
        source='offered_book'
    )

    requester = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = BookRequest
        fields = [
            'id', 'request_type', 'status', 
            'requested_book', 'requested_book_id',
            'offered_book', 'offered_book_id',
            'requester', 'expected_return_date',
            'requester_notes', 'owner_notes',
            'request_date', 'response_date'
        ]
        extra_kwargs = {
            'expected_return_date': {'required': False},
            'status': {'read_only': True},
            'response_date': {'read_only': True},
        }


        def validate(self, data):
            if data['request_type'] == 'swap' and 'offered_book' not in data:
                raise serializers.ValidationError("Swap requests require an offered book")
            
            if data['request_type'] == 'borrow' and 'expected_return_date' not in data:
                raise serializers.ValidationError("Borrow requests require an expected return date")
            
            # verify the requester doesn't own the requested book 
            if data['requested_book'].owner == data['requester']:
                raise serializers.ValidationError("You cannot request your own book")
            
            return data