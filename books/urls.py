from django.urls import path, include
from rest_framework import routers
from .views import BookViewSet, GenreViewset


# ROUTERS
router = routers.DefaultRouter()
router.register(r'books', BookViewSet, basename='book')
router.register(r'genres', GenreViewset, basename='genre')

# urls 
urlpatterns = [
    path('', include(router.urls))
]
