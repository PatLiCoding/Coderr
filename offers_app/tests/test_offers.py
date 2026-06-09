from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from auth_app.models import User
from offers_app.models import Offer, OfferDetail
from offers_app.tests.test_data import VALID_OFFER_POST_DATA, \
    VALID_OFFER_PATCH_DATA


class OffersTestsHappyPath(APITestCase):
    """
    Test suite executing happy path operations for the Offers application
    endpoints.

    Verifies that an authorized user with appropriate roles can perform
    standard CRUD operations and receive expected successful HTTP status
    codes.
    """

    def setUp(self):
        """
        Initializes the test environment and database fixtures before each
        test method.

        Actions performed:
            1. Creates a business-type user account.
            2. Generates an active base Offer object instance.
            3. Attaches three variations of nested OfferDetails (basic,
            standard, premium).
            4. Generates an authentication token and attaches it to the
            API test client.
        """
        self.user = User.objects.create_user(
            username='testuser', password='testpassword123',
            first_name='firstname', last_name='lastname',
            type='business')
        self.offer = Offer.objects.create(
            user=self.user, title='Test', description='Test',
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
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get_list_offers_return_200(self):
        """
        Verifies that a GET request to the main offers endpoint returns an
        HTTP 200 OK status.
        """
        self.url = reverse('offers')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_offer_return_200(self):
        """
        Verifies that a GET request to retrieve a specific offer by ID returns
        an HTTP 200 OK status.
        """
        self.url = reverse('offer-detail', kwargs={'offer_id': self.offer.id})
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_offerdetail_return_200(self):
        """
        Verifies that a GET request to fetch detailed variations of an offer
        returns an HTTP 200 OK status.
        """
        self.url = reverse('offerdetail-detail',
                           kwargs={'offerdetail_id': self.offerdetail1.id})
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_offer_return_201(self):
        """
        Verifies that a POST request containing valid payload data successfully
        creates a new Offer (HTTP 201 Created).
        """
        self.url = reverse('offers')
        response = self.client.post(
            self.url, VALID_OFFER_POST_DATA, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_patch_offer_return_200(self):
        """
        Verifies that a PATCH request containing valid partial data
        successfully updates an existing Offer (HTTP 200 OK).
        """
        self.url = reverse('offer-detail', kwargs={'offer_id': self.offer.id})
        response = self.client.patch(
            self.url, VALID_OFFER_PATCH_DATA, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_offer_return_204(self):
        """
        Verifies that a DELETE request targetting a specific offer removes it
        and returns an HTTP 204 No Content status.
        """
        self.url = reverse('offer-detail', kwargs={'offer_id': self.offer.id})
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
