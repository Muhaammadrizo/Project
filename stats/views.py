from rest_framework import viewsets, status, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count, Sum
from .models import ViewStats, Wishlist
from .serializers import (
    ViewStatsSerializer,
    WishlistSerializer,
    WishlistCreateSerializer,
    DashboardStatsSerializer
)
from products.models import Product
from leads.models import Lead


class ViewStatsViewSet(viewsets.ModelViewSet):
    """ViewSet for product view statistics"""
    queryset = ViewStats.objects.all()
    serializer_class = ViewStatsSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['views_count', 'likes_count', 'created_at']

    def list(self, request, *args, **kwargs):
        """List all product statistics"""
        stats = ViewStats.objects.all().order_by('-views_count')
        serializer = self.get_serializer(stats, many=True)
        return Response(serializer.data)


class WishlistViewSet(viewsets.ModelViewSet):
    """
    ViewSet for wishlist/likes
    - list: GET /wishlist
    - create: POST /wishlist
    - destroy: DELETE /wishlist/:id
    """
    queryset = Wishlist.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['product__name', 'session_id']

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'create':
            return WishlistCreateSerializer
        return WishlistSerializer

    def get_queryset(self):
        """Filter wishlist by session_id if provided"""
        queryset = Wishlist.objects.all()
        session_id = self.request.query_params.get('session_id', None)
        
        if session_id:
            queryset = queryset.filter(session_id=session_id)
        
        return queryset

    def create(self, request, *args, **kwargs):
        """Add product to wishlist"""
        data = request.data.copy()
        
        # Set session_id from request or params
        if not data.get('session_id'):
            data['session_id'] = request.query_params.get('session_id', '')
        
        # Check if product is already in wishlist
        product_id = data.get('product')
        session_id = data.get('session_id')
        
        if Wishlist.objects.filter(
            product_id=product_id,
            session_id=session_id
        ).exists():
            # Remove from wishlist if already exists
            Wishlist.objects.filter(
                product_id=product_id,
                session_id=session_id
            ).delete()
            return Response(
                {'detail': 'Removed from wishlist'},
                status=status.HTTP_200_OK
            )
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    @staticmethod
    def destroy(request, *args, **kwargs):
        """Remove product from wishlist"""
        instance = WishlistViewSet.queryset.get(pk=kwargs['pk'])
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    @api_view(['GET'])
    def wishlist_status(request):
        """Check if product is in wishlist"""
        product_id = request.query_params.get('product_id')
        session_id = request.query_params.get('session_id', '')
        
        if not product_id:
            return Response(
                {'error': 'product_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        is_in_wishlist = Wishlist.objects.filter(
            product_id=product_id,
            session_id=session_id
        ).exists()
        
        return Response({
            'product_id': product_id,
            'is_in_wishlist': is_in_wishlist
        })


@api_view(['GET'])
def dashboard_stats(request):
    """Get dashboard statistics for admin"""
    try:
        # Get basic counts
        total_products = Product.objects.count()
        total_views = ViewStats.objects.aggregate(Sum('views_count'))['views_count__sum'] or 0
        total_likes = ViewStats.objects.aggregate(Sum('likes_count'))['likes_count__sum'] or 0
        total_leads = Lead.objects.count()
        
        # Get top viewed products
        top_viewed = ViewStats.objects.filter(
            views_count__gt=0
        ).order_by('-views_count')[:5]
        top_viewed_data = [
            {
                'id': stat.product.id,
                'name': stat.product.name,
                'model': stat.product.model,
                'views': stat.views_count
            }
            for stat in top_viewed
        ]
        
        # Get top liked products
        top_liked = ViewStats.objects.filter(
            likes_count__gt=0
        ).order_by('-likes_count')[:5]
        top_liked_data = [
            {
                'id': stat.product.id,
                'name': stat.product.name,
                'model': stat.product.model,
                'likes': stat.likes_count
            }
            for stat in top_liked
        ]
        
        # Get recent leads
        recent_leads = Lead.objects.select_related('product').order_by('-created_at')[:10]
        recent_leads_data = [
            {
                'id': lead.id,
                'full_name': lead.full_name,
                'phone': lead.phone,
                'product_name': lead.product.name,
                'created_at': lead.created_at
            }
            for lead in recent_leads
        ]
        
        return Response({
            'total_products': total_products,
            'total_views': total_views,
            'total_likes': total_likes,
            'total_leads': total_leads,
            'top_viewed_products': top_viewed_data,
            'top_liked_products': top_liked_data,
            'recent_leads': recent_leads_data
        })
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
