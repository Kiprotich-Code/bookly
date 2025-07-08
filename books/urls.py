from django.urls import path, include
from rest_framework import routers
from .views import BookViewSet, GenreViewset


# ROUTERS
router = routers.DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'genres', GenreViewset)

# urls 
urlpatterns = [
    path('', include(router.urls))
]
