from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    """
    Custom user model that extends the default Django AbstractUser.
    Includes a 'type' field to distinguish between different user roles
    (Customer or Business).
    """
    USER_TYPES = (
        ('customer', 'Customer'),
        ('business', 'Business'),
    )

    type = models.CharField(
        max_length=20, choices=USER_TYPES, default='customer')

    def __str__(self):
        """
        Returns the username of the associated user as the string
        representation.
        """
        return self.username
