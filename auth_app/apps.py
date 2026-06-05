from django.apps import AppConfig


class AuthAppConfig(AppConfig):
    """
    Application configuration for the 'auth_app' application.
    Handles application initialization routines and signal connection.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auth_app'

    def ready(self):
        """
        Called when the application registry is fully loaded.
        Imports and activates application-specific signals.
        """
        import auth_app.signals
        _ = auth_app.signals
