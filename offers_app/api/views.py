from rest_framework.generics import ListAPIView, RetrieveAPIView
from offers_app.api.serializers import OffersListSerializer, \
    OfferSerializer, OfferDetailSerializer
from offers_app.models import Offer, OfferDetail


class OffersListView(ListAPIView):
    serializer_class = OffersListSerializer
    queryset = Offer.objects.all()


class OfferView(RetrieveAPIView):
    serializer_class = OfferSerializer
    queryset = Offer.objects.all()
    lookup_url_kwarg = 'offer_id'


class OfferDetailView(RetrieveAPIView):
    serializer_class = OfferDetailSerializer
    queryset = OfferDetail.objects.all()
    lookup_url_kwarg = 'offerdetail_id'
