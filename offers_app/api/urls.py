"""
URL Configuration for the Offers application.

This module routes incoming HTTP requests to the appropriate Class-Based
Views (CBVs).

Endpoints:
    - /offers/ :
        Handles listing existing offers and creating new ones.
        Name: 'offers'
    - /offers/<offer_id>/ :
        Handles retrieving, updating, or deleting a specific offer instance
        by ID.
        Name: 'offer-detail'
    - /offerdetails/<offerdetail_id>/ :
        Handles retrieving, updating, or deleting granular sub-details of an
        offer by ID.
        Name: 'offerdetail-detail'
"""
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
