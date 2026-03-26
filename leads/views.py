from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Lead
from .serializers import (
    LeadSerializer,
    LeadCreateSerializer,
    LeadListSerializer
)


class LeadViewSet(viewsets.ModelViewSet):
    """
    ViewSet for leads (contact submissions)
    - list: GET /leads (admin only)
    - create: POST /leads
    - retrieve: GET /leads/:id (admin only)
    - destroy: DELETE /leads/:id (admin only)
    """
    queryset = Lead.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['full_name', 'phone', 'product__name']
    ordering_fields = ['created_at', 'full_name']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'create':
            return LeadCreateSerializer
        elif self.action == 'list':
            return LeadListSerializer
        return LeadSerializer

    def create(self, request, *args, **kwargs):
        """Create a new lead"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        # Return full serialized data with product info
        lead = Lead.objects.get(id=serializer.data['id'])
        response_serializer = LeadSerializer(lead)
        
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    @action(detail=False, methods=['get'])
    def product_leads(self, request):
        """Get leads for a specific product"""
        product_id = request.query_params.get('product_id', None)
        
        if product_id is None:
            return Response(
                {'error': 'product_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        leads = Lead.objects.filter(product_id=product_id)
        serializer = LeadListSerializer(leads, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def total_leads(self, request):
        """Get total number of leads"""
        total = Lead.objects.count()
        return Response({
            'total_leads': total
        })

    @action(detail=False, methods=['get'])
    def leads_by_product(self, request):
        """Get leads count grouped by product"""
        from django.db.models import Count
        
        leads_data = Lead.objects.values(
            'product__id',
            'product__name',
            'product__model'
        ).annotate(count=Count('id')).order_by('-count')
        
        return Response(leads_data)
