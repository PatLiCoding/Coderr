from django.urls import path
from .views import OffersListView, OfferView, OfferDetailView

urlpatterns = [
    path('offers/', OffersListView.as_view(), name='offers'),
    path(
        'offers/<int:offer_id>/',
        OfferView.as_view(),
        name='offer-detail'
    ),
    path(
        'offerdetails/<int:offerdetail_id>/',
        OfferDetailView.as_view(),
        name='offerdetail-detail'
    ),
]
