from rest_framework import serializers
from django.shortcuts import get_object_or_404
from offers_app.models import OfferDetail
from orders_app.models import Order


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying comprehensive order information.
    Flattens read-only related attributes directly from the linked
    OfferDetail model.
    """
    title = serializers.CharField(source='offer_detail.title')
    revisions = serializers.IntegerField(source='offer_detail.revisions')
    delivery_time_in_days = serializers.IntegerField(
        source='offer_detail.delivery_time_in_days')
    price = serializers.DecimalField(
        source='offer_detail.price', max_digits=10,
        decimal_places=2)
    features = serializers.ListField(source='offer_detail.features')
    offer_type = serializers.CharField(source='offer_detail.offer_type')

    class Meta:
        model = Order
        fields = [
            'id', 'customer_user', 'business_user', 'title',
            'revisions', 'delivery_time_in_days', 'price',
            'features', 'offer_type', 'status', 'created_at',
            'updated_at',
        ]


class OrderCreateSerializer(serializers.Serializer):
    """
    Serializer dedicated to validating and processing new order
    creation entries.
    """
    offer_detail_id = serializers.IntegerField()

    def create(self, validated_data):
        """
        Resolves offer references and creates a new Order record instance.

        Infers the ordering customer from the active session and assigns the
        associated business user automatically based on the chosen offer
        details.

        Args:
            validated_data (dict): Cleaned and validated payload dictionary.

        Returns:
            Order: The newly initialized Order model database instance.
        """
        request = self.context['request']
        offer_detail = get_object_or_404(
            OfferDetail,
            id=validated_data['offer_detail_id']
        )
        return Order.objects.create(
            customer_user=request.user,
            business_user=offer_detail.offer.user,
            offer_detail=offer_detail,
            status='in_progress'
        )


class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer optimized strictly for mutating state progression paths
    on existing Orders, preventing any side fields pollution.
    """
    class Meta:
        model = Order
        fields = ['status']

    def validate_status(self, value):
        """
        Validates that the incoming status value conforms to the application
        ruleset.

        Args:
            value (str): The state value proposed in the payload.

        Raises:
            serializers.ValidationError: If the value is not in the allowed
            pool.

        Returns:
            str: The confirmed valid state string.
        """
        allowed = ['in_progress', 'completed', 'cancelled']
        if value not in allowed:
            raise serializers.ValidationError("Invalid status.")
        return value

    def validate(self, attrs):
        """
        Validates overall structural components to explicitly forbid
        extraneous keys.

        Args:
            attrs (dict): Dictionary of validated input attributes.

        Raises:
            serializers.ValidationError: If foreign data is mixed into the
            request.

        Returns:
            dict: The validated attributes dataset.
        """
        unknown = set(self.initial_data) - set(self.fields)
        if unknown:
            raise serializers.ValidationError(
                {k: "Invalid field." for k in unknown}
            )
        return attrs

    def update(self, instance, validated_data):
        """
        Persists state transitions safely onto the targeted Order instance.

        Args:
            instance (Order): The current Order database record instance.
            validated_data (dict): Validated safe input dataset.

        Returns:
            Order: The updated Order database instance.
        """
        instance.status = validated_data['status']
        instance.save()
        return instance
