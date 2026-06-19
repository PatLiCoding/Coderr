from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from auth_app.models import User
from offers_app.models import Offer, OfferDetail
from offers_app.tests.test_data import VALID_OFFER_POST_DATA, \
    VALID_OFFER_PATCH_DATA, INVALID_PAYLOAD_SINGLE_DETAIL, \
    INVALID_PAYLOAD_DUPLICATE_TYPES, INVALID_PAYLOAD_NON_EXISTENT_OFFER_TYPE


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


class OffersTestsUnhappyPath(APITestCase):
    """
    Test suite executing unhappy path and edge-case operations for the Offers
    application endpoints.

    Verifies that the API correctly handles unauthenticated requests,
    unauthorized actions, invalid payloads, and non-existent resources.
    """

    def setUp(self):
        """
        Initializes the test environment with an existing offer and a regular
        customer user to test permission boundaries.
        """
        self.business_user = User.objects.create_user(
            username='bizuser', password='testpassword123', type='business')

        self.offer = Offer.objects.create(
            user=self.business_user, title='Existing Offer',
            description='Test', min_price=10.00, min_delivery_time=5)
        self.customer_user = User.objects.create_user(
            username='customeruser', password='testpassword123',
            type='customer')
        self.customer_token = Token.objects.create(user=self.customer_user)

    def test_get_non_existent_offer_returns_404(self):
        """
        Verifies that requesting an offer ID that does not exist returns
        404 Not Found.
        """
        self.url = reverse('offer-detail', kwargs={'offer_id': 99999})
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_post_returns_401(self):
        """
        Verifies that creating an offer without an authentication token
        returns 401 Unauthorized.
        """
        self.client.credentials()
        self.url = reverse('offers')
        response = self.client.post(
            self.url, VALID_OFFER_POST_DATA, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_customer_user_cannot_create_offer_returns_403(self):
        """
        Verifies that a user with type 'customer' is forbidden from creating
        an offer.
        """
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        self.url = reverse('offers')
        response = self.client.post(
            self.url, VALID_OFFER_POST_DATA, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_invalid_offer_data_returns_400(self):
        """
        Verifies that sending an invalid/empty payload returns 400 Bad Request.
        """
        business_token = Token.objects.create(user=self.business_user)
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + business_token.key)
        self.url = reverse('offers')
        invalid_data = {'title': ''}
        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_offer_with_only_one_detail_returns_400(self):
        """
        Test that a POST with only one OfferDetail fails (HTTP 400).
        """
        business_token = Token.objects.create(user=self.business_user)
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + business_token.key)
        self.url = reverse('offers')
        response = self.client.post(
            self.url, INVALID_PAYLOAD_SINGLE_DETAIL, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('details', response.data)

    def test_create_offer_with_duplicate_detail_types_returns_400(self):
        """
        Tests that a POST with duplicate offer_types fails (HTTP 400),
        even if a total of 3 elements are sent.
        """
        business_token = Token.objects.create(user=self.business_user)
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + business_token.key)
        self.url = reverse('offers')
        count_before = Offer.objects.count()
        response = self.client.post(
            self.url, INVALID_PAYLOAD_DUPLICATE_TYPES, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('details', response.data)
        self.assertEqual(Offer.objects.count(), count_before)

    def test_patch_offer_of_different_owner_returns_403_or_404(self):
        """
        Verifies that a user cannot modify an offer they do not own.
        Depending on your architecture, this should return 403 Forbidden
        (or 404 if you filter queries by request.user).
        """
        other_business = User.objects.create_user(
            username='otherbiz', password='testpassword123', type='business')
        other_token = Token.objects.create(user=other_business)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + other_token.key)
        self.url = reverse('offer-detail', kwargs={'offer_id': self.offer.id})
        response = self.client.patch(
            self.url, VALID_OFFER_PATCH_DATA, format='json')
        self.assertIn(response.status_code, [
                      status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND])

    def test_patch_offer_patch_non_detail_type_returns_400(self):
        """
        Ensure that a PATCH request returns a 400 Bad Request status code
        if the payload contains a nested detail configuration that lacks
        the mandatory 'offer_type' field.
        """
        business_token = Token.objects.create(user=self.business_user)
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + business_token.key)
        self.url = reverse('offer-detail', kwargs={'offer_id': self.offer.id})
        response = self.client.patch(
            self.url, INVALID_PAYLOAD_NON_EXISTENT_OFFER_TYPE, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
