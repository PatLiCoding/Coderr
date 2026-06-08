from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from offers_app.api.filter import OfferFilter
from offers_app.api.serializers import OffersListSerializer, \
    OfferSerializer, OfferDetailSerializer
from offers_app.models import Offer, OfferDetail
from offers_app.api.pagination import OfferPagination


class OffersListView(ListAPIView):
    serializer_class = OffersListSerializer
    queryset = Offer.objects.all()
    pagination_class = OfferPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = OfferFilter
    ordering_fields = ['updated_at', 'min_price']
    search_fields = ['title', 'description']


class OfferView(RetrieveAPIView):
    serializer_class = OfferSerializer
    queryset = Offer.objects.all()
    lookup_url_kwarg = 'offer_id'


class OfferDetailView(RetrieveAPIView):
    serializer_class = OfferDetailSerializer
    queryset = OfferDetail.objects.all()
    lookup_url_kwarg = 'offerdetail_id'
