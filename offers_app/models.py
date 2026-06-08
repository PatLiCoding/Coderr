from django.db import models
from auth_app.models import User

# Create your models here.


class Offer(models.Model):
    """
    Main offer model.
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='offers')
    title = models.CharField(max_length=255)
    image = models.FileField(upload_to='offers/', null=True, blank=True)
    description = models.TextField()
    min_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    min_delivery_time = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class OfferDetail(models.Model):
    """
    Offer package (basic, standard, premium).
    """
    OFFER_TYPES = [
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium'),
    ]

    offer = models.ForeignKey(
        Offer, on_delete=models.CASCADE, related_name='details')
    title = models.CharField(max_length=255)
    revisions = models.IntegerField(default=0)
    delivery_time_in_days = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(default=list)
    offer_type = models.CharField(
        max_length=10, choices=OFFER_TYPES, default='basic')

    def __str__(self):
        return f"{self.offer.title} - {self.offer_type}"
