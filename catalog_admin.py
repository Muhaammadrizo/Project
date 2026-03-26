"""
Custom admin site configuration
"""
from django.contrib import admin
from django.urls import path
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status as http_status


# Customize admin site
admin.site.site_header = "Electrical Products Catalog Admin"
admin.site.site_title = "Catalog Admin"
admin.site.index_title = "Welcome to Admin Dashboard"


class CatalogAdminSite(admin.AdminSite):
    """Custom admin site"""
    site_header = "Electrical Products Catalog"
    site_title = "Admin"
    index_title = "Dashboard"

    def get_urls(self):
        """Add custom admin URLs"""
        from stats.views import dashboard_stats
        
        urls = super().get_urls()
        custom_urls = [
            path('dashboard-api/', dashboard_stats, name='dashboard-api'),
        ]
        return custom_urls + urls
