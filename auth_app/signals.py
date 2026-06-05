from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from profile_app.models import Profile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal receiver that automatically creates a Profile instance whenever a
    new User is registered.

    Triggered immediately after a User instance is saved. It checks the
    'created' flag to ensure the profile is only initialized during the
    initial user creation.
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal receiver that ensures the associated Profile instance is updated
    whenever the User is saved.

    Safely checks for the existence of the reverse relation ('profil') before
    triggering the save method on the profile instance to prevent errors.
    """
    if hasattr(instance, 'profil'):
        instance.profil.save()
