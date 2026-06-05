from django.urls import path
from .views import ProfilDetailView, BusinessListView, CustomerListView

urlpatterns = [
    path(
        'profile/<int:user_id>/', ProfilDetailView.as_view(), name='profile'),
    path(
        'profiles/business/', BusinessListView.as_view(), name='business'),
    path(
        'profiles/customer/', CustomerListView.as_view(), name='customer'),
]
