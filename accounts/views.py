# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.authtoken.models import Token
from .serializers import EmailAuthSerializer, GoogleAuthSerializer
from rest_framework.decorators import api_view
from allauth.socialaccount.models import SocialAccount
from .models import User

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
            return Response({
                'token': token.key,
                'user_id': user.id,
                'email': user.email,
                'is_google': hasattr(user, 'socialaccount')
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
        

# PASSWORD RESET LOGIC 
# serializers.py
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email not found")
        return value

# views.py
class PasswordResetView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            # Send email with reset link
            # (Implement your email sending logic)
            return Response({'success': True})
        return Response(serializer.errors, status=400)