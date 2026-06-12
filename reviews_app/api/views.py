from rest_framework.generics import ListCreateAPIView, \
    RetrieveUpdateDestroyAPIView
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from reviews_app.api.permissions import IsCustomerOrOwner
from reviews_app.api.serializers import ReviewSerializer, \
    ReviewDetailSerializer
from reviews_app.models import Review


class ReviewsView(ListCreateAPIView):
    """
    View handler for listing feedback collections or submitting new ratings.
    Supports structured filtering by business/reviewer and sorting by date or
    score.
    """
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    permission_classes = [IsCustomerOrOwner]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['business_user', 'reviewer']
    ordering_fields = ['updated_at', 'rating']

    def perform_create(self, serializer):
        """
        Automatically stamp the currently logged-in user as the authoring
        reviewer.
        """
        serializer.save(reviewer=self.request.user)


class ReviewsDetailView(RetrieveUpdateDestroyAPIView):
    """
    View handler for managing targeted review detail instances.
    Provides read, update, and structural delete paths under strict ownership
    validation rules.
    """
    serializer_class = ReviewDetailSerializer
    queryset = Review.objects.all()
    permission_classes = [IsCustomerOrOwner]
    lookup_url_kwarg = 'review_id'
