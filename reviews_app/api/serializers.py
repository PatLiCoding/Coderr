from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from reviews_app.models import Review


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = [
            'id', 'business_user', 'reviewer', 'rating',
            'description', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'reviewer', 'created_at', 'updated_at']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError(code='invalid')
        return value

    def validate(self, data):
        if not self.instance:
            reviewer = self.context['request'].user
            business_user = data.get('business_user')
            if Review.objects.filter(
                    reviewer=reviewer, business_user=business_user).exists():
                raise PermissionDenied()
        return data


class ReviewDetailSerializer(ReviewSerializer):

    class Meta:
        model = Review
        fields = [
            'id', 'business_user', 'reviewer', 'rating',
            'description', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'business_user',
                            'reviewer', 'created_at', 'updated_at']
