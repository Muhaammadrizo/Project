from django.db import models


class Product(models.Model):
    """Product model for electrical products catalog"""
    name = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return f"{self.name} ({self.model})"

    def get_total_views(self):
        """Get total views for this product"""
        try:
            stats = self.stats
            return stats.views_count
        except:
            return 0

    def get_total_likes(self):
        """Get total likes/wishlist count"""
        from stats.models import ViewStats
        try:
            stats = ViewStats.objects.get(product=self)
            return stats.likes_count
        except:
            return 0
