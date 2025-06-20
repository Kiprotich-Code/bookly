from django.urls import path, include
from rest_framework import routers
from .views import BookViewset, GenreViewset

# urls 
router = routers.DefaultRouter()
router.register(r'books', BookViewset)
router.register(r'genres', GenreViewset)

urlpatterns = [
    path('', include(router.urls))
]