from rest_framework import serializers
from .models import ViewStats, Wishlist


class ViewStatsSerializer(serializers.ModelSerializer):
    """Serializer for ViewStats"""
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_model = serializers.CharField(source='product.model', read_only=True)

    class Meta:
        model = ViewStats
        fields = ['id', 'product', 'product_name', 'product_model', 'views_count', 'likes_count', 'created_at']
        read_only_fields = ['id', 'created_at', 'views_count', 'likes_count']


class WishlistSerializer(serializers.ModelSerializer):
    """Serializer for Wishlist"""
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_model = serializers.CharField(source='product.model', read_only=True)
    product_image = serializers.ImageField(source='product.image', read_only=True)

    class Meta:
        model = Wishlist
        fields = ['id', 'product', 'product_name', 'product_model', 'product_image', 'created_at']
        read_only_fields = ['id', 'created_at']


class WishlistCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating wishlist items"""

    class Meta:
        model = Wishlist
        fields = ['product', 'session_id']
        required = ['product']


class DashboardStatsSerializer(serializers.Serializer):
    """Dashboard statistics serializer"""
    total_products = serializers.IntegerField()
    total_views = serializers.IntegerField()
    total_likes = serializers.IntegerField()
    total_leads = serializers.IntegerField()
    top_viewed_products = serializers.ListField()
    top_liked_products = serializers.ListField()
    recent_leads = serializers.ListField()
