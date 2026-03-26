from django.contrib import admin
from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone', 'product', 'created_at']
    list_filter = ['created_at', 'product']
    search_fields = ['full_name', 'phone', 'product__name']
    readonly_fields = ['created_at']
    fieldsets = (
        ('Contact Information', {
            'fields': ('full_name', 'phone')
        }),
        ('Product', {
            'fields': ('product',)
        }),
        ('Timestamp', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    date_hierarchy = 'created_at'
