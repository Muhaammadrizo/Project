from rest_framework import serializers
from .models import Product


class ProductListSerializer(serializers.ModelSerializer):
    """Serializer for product list view (basic info)"""
    views_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'model', 'image', 'views_count', 'likes_count']

    def get_views_count(self, obj):
        """Get views count from stats"""
        try:
            from stats.models import ViewStats
            stats = ViewStats.objects.get(product=obj)
            return stats.views_count
        except:
            return 0

    def get_likes_count(self, obj):
        """Get likes count from stats"""
        try:
            from stats.models import ViewStats
            stats = ViewStats.objects.get(product=obj)
            return stats.likes_count
        except:
            return 0


class ProductDetailSerializer(serializers.ModelSerializer):
    """Serializer for product detail view"""
    views_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'model', 'description', 'image', 'created_at', 'views_count', 'likes_count']

    def get_views_count(self, obj):
        """Get views count from stats"""
        try:
            from stats.models import ViewStats
            stats = ViewStats.objects.get(product=obj)
            return stats.views_count
        except:
            return 0

    def get_likes_count(self, obj):
        """Get likes count from stats"""
        try:
            from stats.models import ViewStats
            stats = ViewStats.objects.get(product=obj)
            return stats.likes_count
        except:
            return 0


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating products"""

    class Meta:
        model = Product
        fields = ['id', 'name', 'model', 'description', 'image']
