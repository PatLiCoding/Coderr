from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from auth_app.models import User
from offers_app.models import Offer, OfferDetail
from orders_app.models import Order


class OdersTestsHappyPath(APITestCase):
    """
    Test suite for successful (happy path) order operations.
    Verifies that standard CRUD operations and custom statistics
    endpoints behave as expected under valid conditions.
    """

    def setUp(self):
        """
        Set up test data including users, an offer, an order,
        and authentication.
        """
        self.business_user = User.objects.create_user(
            username='businessUser', password='testpassword123',
            first_name='firstname', last_name='lastname',
            type='business')
        self.customer_user = User.objects.create_user(
            username='customerUser', password='testpassword123',
            first_name='firstname', last_name='lastname',
            type='customer')
        self.staff_user = User.objects.create_user(
            username='staffUser', password='testpassword123',
            first_name='firstname', last_name='lastname',
            type='business', is_staff=True)
        self.offer = Offer.objects.create(
            user=self.business_user, title='Test', description='Test',
            min_price=12.00, min_delivery_time=3)
        self.offerdetail = OfferDetail.objects.create(
            offer=self.offer, title='Test', revisions=0,
            delivery_time_in_days=3, price=13.0, features=['test1', 'test2'],
            offer_type='basic')
        self.order = Order.objects.create(
            customer_user=self.customer_user, business_user=self.business_user,
            offer_detail=self.offerdetail, status='in_progress')
        self.token = Token.objects.create(user=self.customer_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get_list_oders_return_200(self):
        """
        Ensure an authenticated user can successfully retrieve the orders list.
        """
        self.url = reverse('orders')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_order_return_201(self):
        """
        Ensure a customer can successfully create a new order with
        valid payload.
        """
        self.url = reverse('orders')
        data = {
            "offer_detail_id": 1
        }
        response = self.client.post(
            self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_patch_order_return_200(self):
        """
        Ensure the assigned business user can successfully update the
        order status.
        """
        self.token = Token.objects.create(user=self.business_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.url = reverse('orders-detail', kwargs={'order_id': self.order.id})
        data = {
            "status": "completed"
        }
        response = self.client.patch(
            self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_order_return_204(self):
        """
        Ensure a staff user can successfully delete an order.
        """
        self.token = Token.objects.create(user=self.staff_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.url = reverse(
            'orders-detail', kwargs={'order_id': self.order.id})
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_order_count_business_user_return_200(self):
        """
        Ensure the total order count endpoint for a business user returns
        200 OK.
        """
        self.url = reverse('order-count',
                           kwargs={'business_user_id': self.business_user.id})
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_completed_order_count_business_user_return_200(self):
        """
        Ensure the completed order count endpoint for a business user returns
        200 OK.
        """
        self.url = reverse('completed-order-count',
                           kwargs={'business_user_id': self.business_user.id})
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class OrdersTestsUnhappyPath(APITestCase):
    """
    Test suite for edge cases and error handling (unhappy path).
    Verifies authentication, authorization boundaries, and validation errors.
    """

    def setUp(self):
        """Set up test environment and data for edge-case scenarios."""
        self.business_user = User.objects.create_user(
            username='businessUser', password='testpassword123',
            type='business')
        self.customer_user = User.objects.create_user(
            username='customerUser', password='testpassword123',
            type='customer')
        self.other_customer = User.objects.create_user(
            username='otherCustomer', password='testpassword123',
            type='customer')
        self.offer = Offer.objects.create(
            user=self.business_user, title='Test', description='Test',
            min_price=12.00, min_delivery_time=3)
        self.offerdetail = OfferDetail.objects.create(
            offer=self.offer, title='Test', revisions=0,
            delivery_time_in_days=3, price=13.0,
            features=['test1'], offer_type='basic')
        self.order = Order.objects.create(
            customer_user=self.customer_user, business_user=self.business_user,
            offer_detail=self.offerdetail, status='in_progress')
        self.customer_token = Token.objects.create(user=self.customer_user)

    def test_get_list_orders_unauthenticated_return_401(self):
        """
        Ensure unauthenticated access to the orders list is blocked with a
        401 Unauthorized.
        """
        self.client.credentials()
        url = reverse('orders')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_order_with_non_existing_offer_detail_return_404(self):
        """
        Ensure creating an order with a non-existent offer detail ID returns a
        404 Not Found.
        """
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        url = reverse('orders')
        data = {"offer_detail_id": 99999}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_order_missing_payload_return_400(self):
        """
        Ensure creating an order with an empty request body returns a
        400 Bad Request.
        """
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        url = reverse('orders')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_order_non_owner_business_return_403(self):
        """
        Ensure a business user who does not own the order is forbidden from
        modifying its status.
        """
        wrong_business = User.objects.create_user(
            username='wrongBusiness', password='password', type='business')
        wrong_token = Token.objects.create(user=wrong_business)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + wrong_token.key)
        url = reverse('orders-detail', kwargs={'order_id': self.order.id})
        data = {"status": "completed"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_order_invalid_status_return_400(self):
        """
        Ensure updating an order with an invalid/unsupported status value
        returns a 400 Bad Request.
        """
        business_token = Token.objects.create(user=self.business_user)
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + business_token.key)

        url = reverse('orders-detail', kwargs={'order_id': self.order.id})
        data = {"status": "fancy_invalid_status"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_order_as_non_staff_return_403(self):
        """
        Ensure regular customers or business users without staff privileges
        can not delete orders.
        """
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        url = reverse('orders-detail', kwargs={'order_id': self.order.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_non_existing_order_return_404(self):
        """
        Ensure attempting to delete a non-existent order returns a
        404 Not Found.
        """
        staff_user = User.objects.create_user(
            username='staff', password='password',
            type='business', is_staff=True)
        staff_token = Token.objects.create(user=staff_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + staff_token.key)

        url = reverse('orders-detail', kwargs={'order_id': 99999})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_order_count_for_non_existing_user_return_404(self):
        """
        Ensure querying the order count for a non-existent user ID returns a
        404 Not Found.
        """
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        url = reverse('order-count', kwargs={'business_user_id': 99999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
