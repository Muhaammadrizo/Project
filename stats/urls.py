from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ViewStatsViewSet, WishlistViewSet, dashboard_stats

router = DefaultRouter()
router.register(r'stats', ViewStatsViewSet, basename='stat')
router.register(r'wishlist', WishlistViewSet, basename='wishlist')

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', dashboard_stats, name='dashboard-stats'),
]
