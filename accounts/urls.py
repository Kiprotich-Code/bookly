from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import AuthView, LogoutView, verify_token, PasswordResetView, LinkAccountView, UserProfileView

urlpatterns = [
    # Authentication
    path('', AuthView.as_view(), name='auth'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/password/reset/', PasswordResetView.as_view(), name='password-reset'),
    path('auth/link-account/', LinkAccountView.as_view(), name='link-account'),
    
    # User Profile
    # path('user/profile/', UserProfileView.as_view(), name='user-profile'),
    
    # Token verification
    path('auth/verify/', verify_token, name='token-verify'),
]