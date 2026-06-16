from django.db import models
from auth_app.models import User
from offers_app.models import OfferDetail

# Create your models here.


class Order(models.Model):
    """
    Database entity representing consumer transactions.
    Binds buyers, creators, specific offer packages, and status progression
    metrics.
    """
    STATUS_CHOICES = [
        ('in_progress', 'In progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    customer_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='orders_as_customer')
    business_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='orders_as_business')
    offer_detail = models.ForeignKey(
        OfferDetail, on_delete=models.PROTECT, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='in_progress')

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        """
        Return the standard readable string pattern format identification
        representation.
        """
        return f"Order {self.id}"
