
from django.urls import path
from .views import ReviewsView, ReviewsDetailView

urlpatterns = [
    path('reviews/', ReviewsView.as_view(), name='reviews'),
    path(
        'reviews/<int:review_id>/',
        ReviewsDetailView.as_view(),
        name='reviews-detail'),
]
