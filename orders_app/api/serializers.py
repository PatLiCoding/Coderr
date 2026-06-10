from rest_framework import serializers
from orders_app.models import Order


class OrdersSerializer(serializers.ModelSerializer):
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
