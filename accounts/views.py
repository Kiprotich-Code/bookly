# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers, generics
from rest_framework.authtoken.models import Token
from .serializers import EmailAuthSerializer, GoogleAuthSerializer, PasswordResetSerializer, RegisterSerializer, UserProfileSerializer
from rest_framework.decorators import api_view
from allauth.socialaccount.models import SocialAccount
from .models import User
from rest_framework.permissions import IsAuthenticated

# REGISTER NEW USERS 
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                'token': token.key,
                'user_id': user.id,
                'email': user.email,
                'is_profile_complete': user.is_profile_complete
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AuthView(APIView):
    def post(self, request):
        auth_type = request.data.get('type')
        
        if auth_type == 'email':
            serializer = EmailAuthSerializer(data=request.data)
        elif auth_type == 'google':
            serializer = GoogleAuthSerializer(data=request.data)
        else:
            return Response(
                {'error': 'Invalid auth type'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if serializer.is_valid():
            user = serializer.validated_data
            token, created = Token.objects.get_or_create(user=user)

            # Get first name if available 
            first_name = getattr(user, 'first_name', '')

            return Response({
                'token': token.key,
                'user_id': user.id,
                'email': user.email,
                'is_google': hasattr(user, 'socialaccount'),
                'is_profile_complete': user.is_profile_complete,
                'first_name': first_name
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# TOKEN VERIFICATION 
@api_view(['GET'])
def verify_token(request):
    return Response({
        'user_id': request.user.id,
        'email': request.user.email,
        'is_google': hasattr(request.user, 'socialaccount')
    })

# LOGOUT VIEW 
class LogoutView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        # Delete the token
        request.user.auth_token.delete()
        return Response({'success': True})
    

# DON'T CREATE ACCOUNT IF IT EXIST 
# views.py
class LinkAccountView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        token = request.data.get('token')
        try:
            idinfo = verify_token(token)
            if SocialAccount.objects.filter(uid=idinfo['sub']).exists():
                return Response(
                    {'error': 'Google account already linked'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            SocialAccount.objects.create(
                user=request.user,
                provider='google',
                uid=idinfo['sub']
            )
            return Response({'success': True})
        except ValueError:
            return Response(
                {'error': 'Invalid token'},
                status=status.HTTP_400_BAD_REQUEST
            )

# views.py
class PasswordResetView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            # Send email with reset link
            # (Implement your email sending logic)
            return Response({'success': True})
        return Response(serializer.errors, status=400)
    

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        Retrieve the authenticated user's profile
        """
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    
    def patch(self, request):
        """
        Update the authenticated user's profile (partial update)
        """
        serializer = UserProfileSerializer(
            request.user, 
            data=request.data, 
            partial=True
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)