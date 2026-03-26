from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Product
from .serializers import (
    ProductListSerializer,
    ProductDetailSerializer,
    ProductCreateUpdateSerializer
)
from stats.models import ViewStats


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for products
    - list: GET /products
    - create: POST /products (admin only)
    - retrieve: GET /products/:id
    - update: PUT /products/:id (admin only)
    - destroy: DELETE /products/:id (admin only)
    """
    queryset = Product.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'model', 'description']
    ordering_fields = ['created_at', 'name']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'retrieve':
            return ProductDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ProductCreateUpdateSerializer
        return ProductListSerializer

    def retrieve(self, request, *args, **kwargs):
        """Override retrieve to track views"""
        response = super().retrieve(request, *args, **kwargs)
        
        # Track product view
        product = self.get_object()
        try:
            stats, created = ViewStats.objects.get_or_create(product=product)
            stats.views_count += 1
            stats.save()
        except Exception as e:
            print(f"Error tracking view: {e}")
        
        return response

    @action(detail=False, methods=['get'])
    def top_viewed(self, request):
        """Get top 5 most viewed products"""
        from stats.models import ViewStats
        
        top_products = ViewStats.objects.filter(
            views_count__gt=0
        ).order_by('-views_count')[:5]
        
        products = [stat.product for stat in top_products]
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def top_liked(self, request):
        """Get top 5 most liked/wishlist products"""
        from stats.models import ViewStats
        
        top_products = ViewStats.objects.filter(
            likes_count__gt=0
        ).order_by('-likes_count')[:5]
        
        products = [stat.product for stat in top_products]
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def view_product(self, request, pk=None):
        """Manually track a product view"""
        product = self.get_object()
        try:
            stats, created = ViewStats.objects.get_or_create(product=product)
            stats.views_count += 1
            stats.save()
            return Response({
                'status': 'success',
                'views': stats.views_count
            })
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
