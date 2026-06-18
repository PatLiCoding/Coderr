from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, \
    RetrieveUpdateDestroyAPIView
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny
from django.db.models import Min
from django_filters.rest_framework import DjangoFilterBackend
from offers_app.api.filter import OfferFilter
from offers_app.api.serializers import OffersListSerializer, \
    OfferCreateSerializer, OfferSerializer, OfferUpdateSerializer, \
    OfferDetailSerializer
from offers_app.models import Offer, OfferDetail
from offers_app.api.pagination import OfferPagination
from offers_app.api.permissions import IsBusinessOrOwner


class OffersListView(ListCreateAPIView):
    """
    API endpoint allowing clients to list existing offers or create a
    new offer.

    Features:
        - Strict permission filtering utilizing `IsBusinessOrOwner`.
        - Paginated listings using `OfferPagination`.
        - Advanced dynamic querying filters (DjangoFilter, Ordering,
            Text Searching).
    """
    serializer_class = OffersListSerializer
    queryset = Offer.objects.all()
    permission_classes = [IsBusinessOrOwner]
    pagination_class = OfferPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = OfferFilter
    ordering_fields = ['updated_at',]
    search_fields = ['title', 'description']

    def get_queryset(self):
        """
        Calculates the minimum price in real-time and ensures guaranteed
        sorting so that pagination runs stably.
        """
        queryset = Offer.objects.annotate(
            annotated_min_price=Min('details__price'),
            annotated_min_delivery_time=Min('details__delivery_time_in_days'))
        ordering = self.request.query_params.get('ordering', '')
        if ordering == 'min_price':
            return queryset.order_by('annotated_min_price')
        elif ordering == '-min_price':
            return queryset.order_by('-annotated_min_price')
        elif ordering == 'updated_at':
            return queryset.order_by('updated_at')
        elif ordering == '-updated_at':
            return queryset.order_by('-updated_at')
        return queryset.order_by('-id')

    def get_permissions(self):
        """
        Dynamic authorization:
        - GET (List): Accessible to everyone (no permissions required).
        - POST (Create): Only logged-in business users (IsBusinessOrOwner).
        """
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsBusinessOrOwner()]

    def get_serializer_class(self):
        """
        Dynamically decides serializer workflows depending on incoming
        HTTP methods.

        Returns:
            Serializer class: `OfferCreateSerializer` for creation tasks
            (POST), otherwise fallback defaults to `OffersListSerializer`
            (GET).
        """
        if self.request.method == 'POST':
            return OfferCreateSerializer
        return OffersListSerializer


class OfferView(RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, or deleting a targeted individual
    Offer instance.

    Looks up entities directly via matching the configured URL keyword
    arguments (`offer_id`).
    """
    serializer_class = OfferSerializer
    permission_classes = [IsBusinessOrOwner]
    queryset = Offer.objects.all()
    lookup_url_kwarg = 'offer_id'

    def get_serializer_class(self):
        """
        Determines the appropriate serializer class based on the HTTP request
        method.

        Returns a specific serializer for partial updates (PATCH) to control
        allowed fields, and falls back to the standard serializer for other
        methods.

        Returns:
            serializers.BaseSerializer: The serializer class to be used for
                the current request.
        """
        if self.request.method == 'PATCH':
            return OfferUpdateSerializer
        return OfferSerializer


class OfferDetailView(RetrieveAPIView):
    """
    Read-only API endpoint providing read lookup capabilities for individual
    sub-details items.

    Identifies isolated model rows using the primary URL argument
    (`offerdetail_id`).
    """
    serializer_class = OfferDetailSerializer
    permission_classes = [IsBusinessOrOwner]
    queryset = OfferDetail.objects.all()
    lookup_url_kwarg = 'offerdetail_id'
