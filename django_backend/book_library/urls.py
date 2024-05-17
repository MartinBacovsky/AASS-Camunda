from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, RentalViewSet, ReturnViewSet, TrendingViewSet

# Create a router and register your viewsets with it.
router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'rentals', RentalViewSet)  # Ensure this line is present
router.register(r'returns', ReturnViewSet)
router.register(r'trending', TrendingViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
