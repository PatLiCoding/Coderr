from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, \
    RetrieveUpdateDestroyAPIView
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from offers_app.api.filter import OfferFilter
from offers_app.api.serializers import OffersListSerializer, \
    OfferCreateSerializer, OfferSerializer, OfferDetailSerializer
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
    ordering_fields = ['updated_at', 'min_price']
    search_fields = ['title', 'description']

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
