from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from auth_app.models import User
from offers_app.models import Offer, OfferDetail
from orders_app.models import Order


class OdersTestsHappyPath(APITestCase):

    def setUp(self):
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
            type='business')
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
        self.url = reverse('orders')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_order_return_201(self):
        self.url = reverse('orders')
        data = {
            "offer_detail_id": 1
        }
        response = self.client.post(
            self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_patch_order_return_200(self):
        self.token = Token.objects.create(user=self.business_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.url = reverse('orders-detail', kwargs={'order_id': self.offer.id})
        data = {
            "status": "completed"
        }
        response = self.client.patch(
            self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_order_return_204(self):
        self.staff_user.is_staff = True
        self.staff_user.save()
        self.token = Token.objects.create(user=self.staff_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.url = reverse(
            'orders-detail', kwargs={'order_id': self.offer.id})
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_order_count_business_user_return_200(self):
        self.url = reverse('order-count',
                           kwargs={'business_user_id': self.business_user.id})
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_completed_order_count_business_user_return_200(self):
        self.url = reverse('completed-order-count',
                           kwargs={'business_user_id': self.business_user.id})
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# Response Return tests:
    # def test_get_list(self):
    #     url = reverse('orders')
    #     response = self.client.get(url)
    #     print("Data:", response.data)
    #     assert False

    # def test_post(self):
    #     self.url = reverse('orders')
    #     data = {
    #         "offer_detail_id": 1
    #     }
    #     response = self.client.post(
    #         self.url, data, format='json')
    #     print(response.data)
    #     assert False

    # def test_patch(self):
    #     self.token = Token.objects.create(user=self.business_user)
    #     self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    #     self.url = reverse(
    #         'orders-detail', kwargs={'order_id': self.offer.id})
    #     data = {
    #         "status": "completed"
    #     }
    #     response = self.client.patch(
    #         self.url, data, format='json')
    #     print(response.data)
    #     assert False
