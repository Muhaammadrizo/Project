from django.contrib import admin
from .models import ViewStats, Wishlist


@admin.register(ViewStats)
class ViewStatsAdmin(admin.ModelAdmin):
    list_display = ['product', 'views_count', 'likes_count', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['product__name', 'product__model']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Product', {
            'fields': ('product',)
        }),
        ('Statistics', {
            'fields': ('views_count', 'likes_count')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['get_identifier', 'product', 'created_at']
    list_filter = ['created_at', 'product']
    search_fields = ['product__name', 'session_id', 'user__username']
    readonly_fields = ['created_at']
    fieldsets = (
        ('Product', {
            'fields': ('product',)
        }),
        ('User/Session', {
            'fields': ('session_id', 'user')
        }),
        ('Timestamp', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def get_identifier(self, obj):
        """Display user or session identifier"""
        if obj.user:
            return f"User: {obj.user.username}"
        return f"Session: {obj.session_id[:8]}..."
    get_identifier.short_description = 'User/Session'
