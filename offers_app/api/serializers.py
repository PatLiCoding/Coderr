from rest_framework import serializers
from offers_app.models import Offer, OfferDetail


class OfferDetailLinkSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']

    def get_url(self, obj):
        return f"/offerdetails/{obj.id}/"


class OfferDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = OfferDetail
        fields = [
            'title', 'revisions', 'delivery_time_in_days',
            'price', 'features', 'offer_type',
        ]


class OfferSerializer(serializers.ModelSerializer):
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = [
            'id', 'user', 'title', 'image',
            'description', 'created_at', 'updated_at',
            'details', 'min_price', 'min_delivery_time',
        ]

    def get_min_price(self, obj):
        prices = obj.details.values_list('price', flat=True)
        return min(prices) if prices else 0

    def get_min_delivery_time(self, obj):
        times = obj.details.values_list('delivery_time_in_days', flat=True)
        return min(times) if times else 0

    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        self._handle_details_update(instance, details_data)
        return instance

    def _handle_details_update(self, instance, details_data):
        if details_data is not None:
            existing_details = {
                detail.offer_type: detail for detail in instance.details.all()}
            for detail_item in details_data:
                offer_type = detail_item.get('offer_type')
                if offer_type in existing_details:
                    detail_instance = existing_details[offer_type]
                    for attr, value in detail_item.items():
                        setattr(detail_instance, attr, value)
                    detail_instance.save()


class OffersListSerializer(OfferSerializer):
    user_details = serializers.SerializerMethodField()
    details = OfferDetailLinkSerializer(many=True, read_only=True)

    class Meta:
        model = Offer
        fields = [
            'id', 'user', 'title', 'image',
            'description', 'created_at', 'updated_at',
            'details', 'min_price', 'min_delivery_time',
            'user_details',
        ]

    def get_user_details(self, obj):
        return {
            'first_name': obj.user.first_name,
            'last_name': obj.user.last_name,
            'username': obj.user.username,
        }


class OfferCreateSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = [
            'title',
            'image',
            'description',
            'details',
        ]

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        offer = Offer.objects.create(
            user=self.context['request'].user,
            **validated_data
        )
        for detail_data in details_data:
            OfferDetail.objects.create(
                offer=offer,
                **detail_data
            )
        return offer
