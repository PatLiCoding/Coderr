from rest_framework import serializers


class BaseInfoSerializer(serializers.Serializer):
    """
    Serializer to format global system aggregates and metrics.
    Structures read-only platform-wide statistics for public landing
    page dashboards.
    """
    review_count = serializers.IntegerField()
    average_rating = serializers.FloatField()
    business_profile_count = serializers.IntegerField()
    offer_count = serializers.IntegerField()
