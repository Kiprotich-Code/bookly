from django.urls import path, include
from rest_framework import routers
from .views import BookViewset, GenreViewset


# ROUTERS
router = routers.DefaultRouter()
router.register(r'books', BookViewset)
router.register(r'genres', GenreViewset)

# urls 
urlpatterns = [
    path('', include(router.urls))
]
