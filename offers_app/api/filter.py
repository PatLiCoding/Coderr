from django_filters import rest_framework as filters
from offers_app.models import Offer


class OfferFilter(filters.FilterSet):
    """
    FilterSet class for the Offer model.

    Provides query parameter filtering capabilities for Offer lists in the API.

    Attributes:
        creator_id (filters.NumberFilter): Filters offers by the creator's
            user ID. Maps to 'user_id'.
        min_price (filters.NumberFilter): Filters offers greater than or equal
            to the specified price. Uses 'gte' lookup on 'min_price'.
        max_delivery_time (filters.NumberFilter): Filters offers less than or
            equal to the specified delivery time. Uses 'lte' lookup on
            'min_delivery_time'.
    """
    creator_id = filters.NumberFilter(field_name='user_id')
    min_price = filters.NumberFilter(field_name='min_price', lookup_expr='gte')
    max_delivery_time = filters.NumberFilter(
        field_name='min_delivery_time',
        lookup_expr='lte'
    )

    class Meta:
        """Metadata options for OfferFilter."""
        model = Offer
        fields = [
            'creator_id',
            'min_price',
            'max_delivery_time'
        ]
