from django.urls import path, include
from rest_framework import routers
from .views import BookRequestViewSet

# routers 
router = routers.DefaultRouter()
router.register(r'', BookRequestViewSet)

urlpatterns = [
    path('', include(router.urls))
]