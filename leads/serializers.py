from rest_framework import serializers
from .models import Lead


class LeadSerializer(serializers.ModelSerializer):
    """Serializer for Lead model"""
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_model = serializers.CharField(source='product.model', read_only=True)

    class Meta:
        model = Lead
        fields = ['id', 'full_name', 'phone', 'product', 'product_name', 'product_model', 'created_at']
        read_only_fields = ['id', 'created_at']


class LeadCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating leads"""

    class Meta:
        model = Lead
        fields = ['full_name', 'phone', 'product']


class LeadListSerializer(serializers.ModelSerializer):
    """Serializer for listing leads (admin view)"""
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_model = serializers.CharField(source='product.model', read_only=True)
    product_image = serializers.ImageField(source='product.image', read_only=True)

    class Meta:
        model = Lead
        fields = ['id', 'full_name', 'phone', 'product', 'product_name', 'product_model', 'product_image', 'created_at']
