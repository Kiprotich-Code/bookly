# serializers.py
from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from django.conf import settings
from allauth.socialaccount.models import SocialAccount
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

User = get_user_model()

class EmailAuthSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        user = authenticate(
            username=attrs['email'],
            password=attrs['password']
        )
        if not user:
            raise serializers.ValidationError('Invalid credentials')
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