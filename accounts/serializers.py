# serializers.py
from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from django.conf import settings
from allauth.socialaccount.models import SocialAccount
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        user.is_profile_complete = False
        user.save()
        return user


class EmailAuthSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user = authenticate(username=email, password=password)
        if user is None:
            return serializers.ValidationError("Unable to log in with the provided credentials.")
        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")
        data['user'] = user
        return user

class GoogleAuthSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate(self, attrs):
        try:
            idinfo = id_token.verify_oauth2_token(
                attrs['token'],
                google_requests.Request(),
                settings.GOOGLE_CLIENT_ID
            )
            
            # Check if Google user exists
            try:
                social_account = SocialAccount.objects.get(
                    provider='google',
                    uid=idinfo['sub']
                )
                return social_account.user
            except SocialAccount.DoesNotExist:
                # Check if email exists as regular user
                email = idinfo['email']
                if User.objects.filter(email=email).exists():
                    raise serializers.ValidationError(
                        'Email already exists with password login'
                    )
                # Create new user
                user = User.objects.create(
                    email=email,
                    username=email,
                    first_name=idinfo.get('given_name', ''),
                    last_name=idinfo.get('family_name', '')
                )
                SocialAccount.objects.create(
                    user=user,
                    provider='google',
                    uid=idinfo['sub']
                )
                return user
        except ValueError:
            raise serializers.ValidationError('Invalid Google token')
        

# PASSWORD RESET LOGIC 
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email not found")
        return value
    

# USER PROFILE 
class UserProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='username', read_only=True)
    privacy_settings = serializers.JSONField()
    favorite_genres = serializers.JSONField()
    
    class Meta:
        model = User  # or Profile if using OneToOne
        fields = [
            'id', 'username', 'email', 'name',
            'bio', 'location', 'favorite_genres',
            'profile_picture', 'member_since',
            'privacy_settings', 'reading_goal',
            'books_read', 'total_swaps', 'average_rating'
        ]
        read_only_fields = [
            'id', 'username', 'email', 'member_since',
            'books_read', 'total_swaps', 'average_rating'
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.profile_picture:
            data['profile_picture'] = instance.profile_picture.url
            data['avatar'] = instance.profile_picture.url
        return data