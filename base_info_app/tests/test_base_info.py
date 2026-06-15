from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from auth_app.models import User
from reviews_app.models import Review
from offers_app.models import Offer, OfferDetail


class BaseInfoTestsHappyPath(APITestCase):
    """
    Test suite verifying public analytical dashboard counters.
    Ensures that mathematical averages are calculated properly and rounded
    correctly.
    """

    def setUp(self):
        """
        Construct mock database records for profiles, feedback forms,
        and service catalogs.
        """
        self.business_user = User.objects.create_user(
            username='businessUser', password='testpassword123',
            first_name='firstname', last_name='lastname', type='business')
        self.customer_user = User.objects.create_user(
            username='customerUser', password='testpassword123',
            first_name='firstname', last_name='lastname', type='customer')
        self.review = Review.objects.create(
            reviewer=self.customer_user, business_user=self.business_user,
            rating=4, description="Alles war toll!")
        self.offer = Offer.objects.create(
            user=self.business_user, title='Test', description='Test',
            min_price=12.00, min_delivery_time=3)
        self.offerdetail1 = OfferDetail.objects.create(
            offer=self.offer, title='Test', revisions=0,
            delivery_time_in_days=3, price=13.0, features=['test1', 'test2'],
            offer_type='basic')
        self.offerdetail2 = OfferDetail.objects.create(
            offer=self.offer, title='Test', revisions=0,
            delivery_time_in_days=3, price=13.0, features=['test1', 'test2'],
            offer_type='standard')
        self.offerdetail3 = OfferDetail.objects.create(
            offer=self.offer, title='Test', revisions=0,
            delivery_time_in_days=3, price=13.0, features=['test1', 'test2'],
            offer_type='premium')
        self.url = reverse('base-info')

    def test_get_base_info_return_200(self):
        """
        Ensure unauthenticated users receive valid global data tracking values
        successfully.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['review_count'], 1)
        self.assertEqual(response.data['average_rating'], 4.0)
        self.assertEqual(response.data['business_profile_count'], 1)
        self.assertEqual(response.data['offer_count'], 1)

    def test_average_rating_is_rounded_to_one_decimal(self):
        """
        Ensure math aggregation logic rounds values accurately to one single
        decimal position.
        """
        Review.objects.create(
            reviewer=self.customer_user, business_user=self.business_user,
            rating=5, description='Test')
        second_customer = User.objects.create_user(
            username='customer2', password='testpassword123',
            first_name='firstname', last_name='lastname',
            type='customer')
        Review.objects.create(
            reviewer=second_customer, business_user=self.business_user,
            rating=5, description='Test')
        response = self.client.get(self.url)
        self.assertEqual(response.data['average_rating'], 4.7)
