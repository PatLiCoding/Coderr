from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from auth_app.models import User
from reviews_app.models import Review


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
        self.review = Review.objects.create(
            reviewer=self.customer_user, business_user=self.business_user,
            rating=4, description="Alles war toll!")
        self.token = Token.objects.create(user=self.customer_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get_reviews_return_200(self):
        self.url = reverse('reviews')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_reviews_return_201(self):
        self.url = reverse('reviews')
        data = {"business_user": 2, "rating": 4,
                "description": "Alles war toll!"}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

# Response Return tests:
    # def test_get_list(self):
    #     self.url = reverse('reviews')
    #     response = self.client.get(self.url)
    #     print("Data:", response.data)
    #     assert False

    # def test_post(self):
    #     self.url = reverse('reviews')
    #     data = {
    #         "business_user": 2,
    #         "rating": 4,
    #         "description": "Alles war toll!"
    #     }
    #     response = self.client.post(
    #         self.url, data, format='json')
    #     print(response.data)
    #     assert False


class OdersTestsUnhappyPath(APITestCase):

    def setUp(self):
        self.business_user = User.objects.create_user(
            username='businessUser', password='testpassword123',
            first_name='firstname', last_name='lastname',
            type='business')
        self.customer_user = User.objects.create_user(
            username='customerUser', password='testpassword123',
            first_name='firstname', last_name='lastname',
            type='customer')
        self.review = Review.objects.create(
            reviewer=self.customer_user, business_user=self.business_user,
            rating=4, description="Alles war toll!")
        self.token = Token.objects.create(user=self.customer_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_post_reviews_return_403(self):
        self.url = reverse('reviews')
        data = {"business_user": self.business_user.id, "rating": 4,
                "description": "Alles war toll!"}
        response = self.client.post(self.url, data, format='json')
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
