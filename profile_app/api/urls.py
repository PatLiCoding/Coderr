from django.urls import path
from .views import ProfilDetailView

urlpatterns = [
    path(
        'profile/<int:user_id>/', ProfilDetailView.as_view(), name='profile'),
]
