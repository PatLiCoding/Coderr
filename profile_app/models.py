from django.db import models
from auth_app.models import User
from profile_app.service import user_profile_path


# Create your models here.


class Profile(models.Model):
    """
    Represents additional profile details linked to a specific User instance.
    Stores professional information, contact details, and uploaded media files.
    """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profil')
    file = models.FileField(upload_to=user_profile_path, null=True, blank=True)
    tel = models.CharField(max_length=20, blank=True, default='')
    location = models.CharField(max_length=100, blank=True, default='')
    description = models.TextField(blank=True, default='')
    working_hours = models.CharField(max_length=20, blank=True, default='')
    email = models.EmailField(max_length=40, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Returns the username of the associated user as the string
        representation.
        """
        return self.user.username
