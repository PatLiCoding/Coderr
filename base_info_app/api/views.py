from django.db.models import Avg
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from auth_app.models import User
from reviews_app.models import Review
from offers_app.models import Offer

from .serializers import BaseInfoSerializer


class BaseInfoView(APIView):
    """
    API view endpoint providing global business performance data metrics.
    Accessible publicly without authentication tokens to populate frontend
    statistics.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        """
        Calculate system aggregates for reviews, ratings, user segments,
        and total listings.
        """
        average_rating = Review.objects.aggregate(
            average=Avg('rating'))['average']
        data = {
            'review_count': Review.objects.count(),
            'average_rating': (
                round(average_rating, 1)
                if average_rating is not None
                else 0.0),
            'business_profile_count': User.objects.filter(
                type='business').count(),
            'offer_count': Offer.objects.count(), }
        serializer = BaseInfoSerializer(data)
        return Response(serializer.data)
