from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'model', 'created_at', 'get_views', 'get_likes']
    list_filter = ['created_at']
    search_fields = ['name', 'model', 'description']
    readonly_fields = ['created_at', 'updated_at', 'get_views', 'get_likes']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'model', 'description')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Statistics', {
            'fields': ('get_views', 'get_likes'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_views(self, obj):
        """Display view count"""
        from stats.models import ViewStats
        try:
            stats = ViewStats.objects.get(product=obj)
            return stats.views_count
        except:
            return 0
    get_views.short_description = 'Total Views'

    def get_likes(self, obj):
        """Display likes count"""
        from stats.models import ViewStats
        try:
            stats = ViewStats.objects.get(product=obj)
            return stats.likes_count
        except:
            return 0
    get_likes.short_description = 'Total Likes'
