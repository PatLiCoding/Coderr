from rest_framework import serializers
from offers_app.models import Offer, OfferDetail


class OfferDetailLinkSerializer(serializers.ModelSerializer):
    """
    Serializer for providing a lightweight link representation of an
    OfferDetail instance.

    Attributes:
        url (serializers.SerializerMethodField): The relative API URL to fetch
            complete details.
    """
    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']

    def get_url(self, obj):
        """
        Generates the relative path URL for the specific OfferDetail instance.

        Args:
            obj (OfferDetail): The current OfferDetail object instance.

        Returns:
            str: Relative URL path string.
        """
        return f"/offerdetails/{obj.id}/"


class OfferDetailAbsoluteLinkSerializer(serializers.ModelSerializer):
    """
    Serializer for providing an absolute URL link representation of an
    OfferDetail instance, utilizing the request context.

    Attributes:
        url (serializers.SerializerMethodField): The absolute API URL including
            domain and protocol.
    """
    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']

    def get_url(self, obj):
        """
        Generates the absolute path URL for the specific OfferDetail instance.

        Args:
            obj (OfferDetail): The current OfferDetail object instance.

        Returns:
            str: Absolute URL path string.
        """
        request = self.context.get("request")
        return request.build_absolute_uri(
            f"/api/offerdetails/{obj.id}/")


class OfferDetailSerializer(serializers.ModelSerializer):
    """
    Standard serializer for complete OfferDetail object data representation.
    Used for full detail views, creation, and mutation.
    """

    class Meta:
        model = OfferDetail
        fields = [
            'id', 'title', 'revisions', 'delivery_time_in_days',
            'price', 'features', 'offer_type',
        ]


class OfferSerializer(serializers.ModelSerializer):
    """
    Comprehensive serializer for Offer objects including nested detail objects.

    Handles retrieval and nested object modifications for individual offers.

    Attributes:
        min_price (serializers.SerializerMethodField): Evaluated lowest price
            among associated details.
        min_delivery_time (serializers.SerializerMethodField): Evaluated
            fastest delivery time among associated details.
        details (OfferDetailAbsoluteLinkSerializer): Nested list of lightweight
            absolute link representations of assigned details.
    """
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    details = OfferDetailAbsoluteLinkSerializer(many=True)

    class Meta:
        model = Offer
        fields = [
            'id', 'user', 'title', 'image',
            'description', 'created_at', 'updated_at',
            'details', 'min_price', 'min_delivery_time',
        ]

    def get_min_price(self, obj):
        """
        Calculates the minimum price among all associated details.

        Args:
            obj (Offer): The current Offer instance.

        Returns:
            int/float: The minimum price found, or 0 if no details exist.
        """
        prices = obj.details.values_list('price', flat=True)
        return min(prices) if prices else 0

    def get_min_delivery_time(self, obj):
        """
        Calculates the shortest delivery time among all associated details.

        Args:
            obj (Offer): The current Offer instance.

        Returns:
            int: The minimum delivery time in days, or 0 if no details exist.
        """
        times = obj.details.values_list('delivery_time_in_days', flat=True)
        return min(times) if times else 0


class OfferUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer optimized for updating an existing Offer instance along with
    its nested OfferDetail components based on their type.
    """
    details = OfferDetailSerializer(many=True, required=False)

    class Meta:
        model = Offer
        fields = [
            'id', 'title', 'image',
            'description', 'details']

    def validate(self, attrs):
        """
        Validates incoming attributes and ensures no unexpected or malicious
        fields are provided in the raw payload.

        Args:
            attrs (dict): Dictionary of validated input attributes.

        Raises:
            serializers.ValidationError: If fields not present in the
            serializer class are provided.

        Returns:
            dict: The validated attributes dataset.
        """
        unknown = set(self.initial_data) - set(self.fields)
        if unknown:
            raise serializers.ValidationError({
                field: "Unknown field."
                for field in unknown
            })
        return attrs

    def update(self, instance, validated_data):
        """
        Updates an existing Offer instance along with its nested details.

        Args:
            instance (Offer): The existing Offer instance to be updated.
            validated_data (dict): Cleaned and validated data dictionary.

        Returns:
            Offer: The updated Offer instance.
        """
        details_data = validated_data.pop('details', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        self._handle_details_update(instance, details_data)
        return instance

    def _handle_details_update(self, instance, details_data):
        """
        Internal helper to update existing nested OfferDetail components based
        on offer_type.

        Args:
            instance (Offer): The parent Offer instance.
            details_data (list of dicts): Validated data structures for nested
            details.
        """
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
    """
    Optimized layout variant of OfferSerializer specialized for list endpoints.

    Replaces deep details structures with lightweight link components and
    embeds generic user data.

    Attributes:
        user_details (serializers.SerializerMethodField):
            Aggregated first/last name and username.
        details (OfferDetailLinkSerializer):
            Simplified referencing URL links.
    """
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
        """
        Constructs a basic user information dictionary profile.

        Args:
            obj (Offer): The current Offer instance.

        Returns:
            dict: Containing 'first_name', 'last_name', and 'username'.
        """
        return {
            'first_name': obj.user.first_name,
            'last_name': obj.user.last_name,
            'username': obj.user.username,
        }


class OfferCreateSerializer(serializers.ModelSerializer):
    """
    Dedicated serializer for handling atomic creation of new Offers and
    related details.
    """
    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = [
            'id', 'title', 'image',
            'description', 'details',
        ]

    def create(self, validated_data):
        """
        Creates a new Offer and simultaneously instantiates all child nested
        details.

        Injects the currently authenticated request user as the primary key
        reference.

        Args:
            validated_data (dict): Cleaned and validated incoming payload data.

        Returns:
            Offer: The newly constructed database model entity instance.
        """
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
