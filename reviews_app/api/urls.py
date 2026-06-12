"""
URL configuration for the reviews application.
Maps resource locations for managing collections and single detail instances.
"""
from django.urls import path
from .views import ReviewsView, ReviewsDetailView

urlpatterns = [
    path('reviews/', ReviewsView.as_view(), name='reviews'),
    path(
        'reviews/<int:review_id>/',
        ReviewsDetailView.as_view(),
        name='reviews-detail'),
]
