from django.db import models
from auth_app.models import User

# Create your models here.


class Review(models.Model):
    """
    Database entity representing business profile reviews.
    Binds a reviewing customer to a target service professional with
    numeric metrics.
    """
    reviewer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='written_reviews')
    business_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='received_reviews')
    rating = models.IntegerField(default=0)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

    def __str__(self):
        """
        Return a readable metadata string format describing the
        review transaction.
        """
        return (
            f"Review by {self.reviewer} for "
            f"{self.business_user} ({self.rating}*)"
        )
