from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from auth_app.models import User
from offers_app.models import Offer, OfferDetail


class OffersTestsHappyPath(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123',
            first_name='firstname',
            last_name='lastname'
        )
        self.offer = Offer.objects.create(
            user=self.user,
            title='Test',
            description='Test',
            min_price=12.00,
            min_delivery_time=3
        )
        self.offerdetail1 = OfferDetail.objects.create(
            offer=self.offer,
            title='Test',
            revisions=0,
            delivery_time_in_days=3,
            price=13.0,
            features=['test1', 'test2'],
            offer_type='basic'
        )
        self.offerdetail2 = OfferDetail.objects.create(
            offer=self.offer,
            title='Test',
            revisions=0,
            delivery_time_in_days=3,
            price=13.0,
            features=['test1', 'test2'],
            offer_type='standard'
        )
        self.offerdetail3 = OfferDetail.objects.create(
            offer=self.offer,
            title='Test',
            revisions=0,
            delivery_time_in_days=3,
            price=13.0,
            features=['test1', 'test2'],
            offer_type='premium'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get_list_offers_return_200(self):
        self.url = reverse('offers')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_offer_return_200(self):
        self.url = reverse('offer-detail', kwargs={'offer_id': self.offer.id})
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_offerdetail_return_200(self):
        self.url = reverse('offerdetail-detail',
                           kwargs={'offerdetail_id': self.offerdetail1.id})
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# Response Return tests:

    # def test_get_list_offers(self):
    #     self.url = reverse('offers')
    #     response = self.client.get(self.url)
    #     print(response.data)
    #     assert False

    # def test_get_offer(self):
    #     self.url = reverse(
    #         'offer-detail', kwargs={'offer_id': self.offer.id})
    #     response = self.client.get(self.url)
    #     print(response.data)
    #     assert False

    # def test_get_offerdetail(self):
    #     self.url = reverse('offerdetail-detail',
    #                        kwargs={'offerdetail_id': self.offerdetail1.id})
    #     response = self.client.get(self.url)
    #     print(response.data)
    #     assert False
