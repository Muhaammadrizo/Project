from django.db import models
from products.models import Product


class ViewStats(models.Model):
    """Model to track product views and likes (wishlist count)"""
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name='stats'
    )
    views_count = models.IntegerField(default=0)
    likes_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'View Stat'
        verbose_name_plural = 'View Stats'

    def __str__(self):
        return f"{self.product.name} - Views: {self.views_count}, Likes: {self.likes_count}"


class Wishlist(models.Model):
    """Model to track individual wishlist items"""
    session_id = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='wishlist_items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='wishlist_entries'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['session_id', 'product'], ['user', 'product']]
        ordering = ['-created_at']
        verbose_name = 'Wishlist Item'
        verbose_name_plural = 'Wishlist Items'

    def __str__(self):
        if self.user:
            return f"{self.user.username} - {self.product.name}"
        return f"Session {self.session_id} - {self.product.name}"

    def save(self, *args, **kwargs):
        """Update ViewStats likes count when wishlist is added"""
        super().save(*args, **kwargs)
        
        # Update the likes count in ViewStats
        try:
            stats, _ = ViewStats.objects.get_or_create(product=self.product)
            stats.likes_count = self.product.wishlist_entries.count()
            stats.save()
        except Exception as e:
            print(f"Error updating likes count: {e}")
