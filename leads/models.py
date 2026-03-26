from django.db import models
from products.models import Product


class Lead(models.Model):
    """Lead model - users who submitted their contact info for a product"""
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='leads'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Lead'
        verbose_name_plural = 'Leads'

    def __str__(self):
        return f"{self.full_name} - {self.phone} ({self.product.name})"
