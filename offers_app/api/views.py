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
    serializer_class = OffersListSerializer
    queryset = Offer.objects.all()
    permission_classes = [IsBusinessOrOwner]
    pagination_class = OfferPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = OfferFilter
    ordering_fields = ['updated_at', 'min_price']
    search_fields = ['title', 'description']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OfferCreateSerializer
        return OffersListSerializer


class OfferView(RetrieveUpdateDestroyAPIView):
    serializer_class = OfferSerializer
    permission_classes = [IsBusinessOrOwner]
    queryset = Offer.objects.all()
    lookup_url_kwarg = 'offer_id'


class OfferDetailView(RetrieveAPIView):
    serializer_class = OfferDetailSerializer
    permission_classes = [IsBusinessOrOwner]
    queryset = OfferDetail.objects.all()
    lookup_url_kwarg = 'offerdetail_id'
