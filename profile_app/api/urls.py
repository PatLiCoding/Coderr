"""
URL routing configuration for user authentication.

Endpoints:
    - POST /registration/ : Registers a new user account and creates an auth
                            token.
    - POST /login/        : Authenticates credentials and returns user data
                            + token.
"""

from django.urls import path
from .views import ProfilDetailView

urlpatterns = [
    path(
        'profile/<int:pk>/', ProfilDetailView.as_view(), name='profile'),
]
