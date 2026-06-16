from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from reviews_app.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """
    Base serializer for handling Review records.
    Includes custom field validation and unique-together checks to prevent
    duplicate submissions from the same customer to the same business.
    """

    class Meta:
        model = Review
        fields = [
            'id', 'business_user', 'reviewer', 'rating',
            'description', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'reviewer', 'created_at', 'updated_at']

    def validate_rating(self, value):
        """
        Ensure the submitted rating value sits inside the standard 1 to 5
        star spectrum.
        """
        if value < 1 or value > 5:
            raise serializers.ValidationError(code='invalid')
        return value

    def validate(self, data):
        """
        Enforce business rules protecting profiles against duplicate reviewer
        entries.
        """
        if not self.instance:
            reviewer = self.context['request'].user
            business_user = data.get('business_user')
            if Review.objects.filter(
                    reviewer=reviewer, business_user=business_user).exists():
                raise PermissionDenied()
        return data


class ReviewDetailSerializer(ReviewSerializer):
    """
    Serializer optimized for individual review detail interactions.

    Locks down the target 'business_user' relation to prevent shifting ratings
    between profiles, ensuring payload safety during updates.
    """

    class Meta:
        model = Review
        fields = [
            'id', 'business_user', 'reviewer', 'rating',
            'description', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'business_user',
                            'reviewer', 'created_at', 'updated_at']

    def validate(self, attrs):
        """
        Validates incoming data to strictly forbid non-editable fields.

        Ensures that clients can only supply fields intended for evaluation
        modifications, throwing explicit errors for any unexpected payload
        contamination.

        Args:
            attrs (dict): Dictionary of validated input attributes.

        Raises:
            serializers.ValidationError: If fields outside of 'rating' and
                'description' are provided in the raw request.

        Returns:
            dict: The validated attributes dataset.
        """
        allowed_fields = {'rating', 'description'}
        received_fields = set(self.initial_data.keys())
        unknown = received_fields - allowed_fields
        if unknown:
            raise serializers.ValidationError(
                {field: "Unknown field." for field in unknown})
        return attrs
