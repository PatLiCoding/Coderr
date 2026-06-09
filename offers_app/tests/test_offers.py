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
            last_name='lastname',
            type='business'
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

    def test_post_offer_return_201(self):
        self.url = reverse('offers')
        data = {
            "title": "Grafikdesign-Paket",
            "image": None,
            "description":
                "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
            "details": [
                {
                    "title": "Basic Design",
                    "revisions": 2,
                    "delivery_time_in_days": 5,
                    "price": 100,
                    "features": [
                        "Logo Design",
                        "Visitenkarte"
                    ],
                    "offer_type": "basic"
                },
                {
                    "title": "Standard Design",
                    "revisions": 5,
                    "delivery_time_in_days": 7,
                    "price": 200,
                    "features": [
                        "Logo Design",
                        "Visitenkarte",
                        "Briefpapier"
                    ],
                    "offer_type": "standard"
                },
                {
                    "title": "Premium Design",
                    "revisions": 10,
                    "delivery_time_in_days": 10,
                    "price": 500,
                    "features": [
                        "Logo Design",
                        "Visitenkarte",
                        "Briefpapier",
                        "Flyer"
                    ],
                    "offer_type": "premium"
                }
            ]
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_patch_offer(self):
        self.url = reverse('offer-detail', kwargs={'offer_id': self.offer.id})
        data = {
            "title": "Updated Grafikdesign-Paket",
            "details": [
                {
                    "title": "Basic Design Updated",
                    "revisions": 3,
                    "delivery_time_in_days": 6,
                    "price": 120,
                    "features": [
                        "Logo Design",
                        "Flyer"
                    ],
                    "offer_type": "basic"
                }
            ]
        }
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_offer(self):
        self.url = reverse('offer-detail', kwargs={'offer_id': self.offer.id})
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
