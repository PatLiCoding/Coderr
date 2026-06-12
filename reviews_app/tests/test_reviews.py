from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from auth_app.models import User
from reviews_app.models import Review


class ReviewTestsHappyPath(APITestCase):
    """
    Test suite for successful (happy path) review operations.
    Verifies standard authenticated CRUD entries flow properly using valid
    payloads.
    """

    def setUp(self):
        """
        Set up environment prerequisites including target roles and
        default entries.
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
        self.token = Token.objects.create(user=self.customer_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get_reviews_return_200(self):
        """
        Ensure an authenticated consumer can successfully list global
        feedback data.
        """
        self.url = reverse('reviews')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_reviews_return_201(self):
        """
        Ensure a valid payload successfully documents a new profile submission.
        """
        self.url = reverse('reviews')
        data = {"business_user": 2, "rating": 4,
                "description": "Alles war toll!"}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_patch_reviews_return_200(self):
        """
        Ensure the feedback owner can update the text details of their
        rating entry.
        """
        self.url = reverse(
            'reviews-detail', kwargs={'review_id': self.review.id})
        data = {"rating": 5, "description": "Noch besser als erwartet!"}
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_review_return_204(self):
        """Ensure the author of a review can successfully delete it."""
        self.url = reverse(
            'reviews-detail', kwargs={'review_id': self.review.id})
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ReviewTestsUnhappyPath(APITestCase):
    """
    Test suite for checking validation boundaries and authorization
    locks (unhappy path).
    Verifies proper status codes on illegal data patterns or
    identity hijacking.
    """

    def setUp(self):
        """
        Set up edge-case testing states including adversarial profile objects.
        """
        self.business_user = User.objects.create_user(
            username='businessUser', password='testpassword123',
            first_name='firstname', last_name='lastname', type='business')
        self.customer_user = User.objects.create_user(
            username='customerUser', password='testpassword123',
            first_name='firstname', last_name='lastname', type='customer')
        self.customer_user2 = User.objects.create_user(
            username='customerUser2', password='testpassword123',
            first_name='firstname', last_name='lastname', type='customer')
        self.review = Review.objects.create(
            reviewer=self.customer_user, business_user=self.business_user,
            rating=4, description="Alles war toll!")
        self.token = Token.objects.create(user=self.customer_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get_reviews_return_401(self):
        """
        Ensure anonymous visitors cannot index or fetch overall reviews lists.
        """
        self.client.credentials()
        self.url = reverse('reviews')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_reviews_return_400_invalid_rating(self):
        """
        Ensure system fields reject arbitrary scores outside valid
        boundaries (e.g., rating=10).
        """
        self.url = reverse('reviews')
        data = {"business_user": self.business_user.id, "rating": 10,
                "description": "Alles war toll!"}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_reviews_return_401(self):
        """
        Ensure entry generation attempts fail immediately if access tokens
        are missing.
        """
        self.client.credentials()
        self.url = reverse('reviews')
        data = {"rating": 5, "description": "Noch besser als erwartet!"}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_business_user_review_return_403(self):
        """
        Ensure service providers/business users are blocked from
        self-reviewing orgiving feedback.
        """
        self.token = Token.objects.create(user=self.business_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.url = reverse('reviews')
        data = {"business_user": self.business_user.id, "rating": 4,
                "description": "Alles war toll!"}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_second_review_for_same_business_return_403(self):
        """
        Ensure a consumer is strictly locked from generating duplicate records
        on a single business.
        """
        self.url = reverse('reviews')
        data = {"business_user": self.business_user.id, "rating": 4,
                "description": "Alles war toll!"}
        response = self.client.post(self.url, data, format='json')
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_reviews_return_400_invalid_rating(self):
        """
        Ensure existing review updates fail if modified scores fall out of
        bounds.
        """
        self.url = reverse(
            'reviews-detail', kwargs={'review_id': self.review.id})
        data = {"rating": 10, "description": "Noch besser als erwartet!"}
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_reviews_return_401(self):
        """
        Ensure updates are rejected with a 401 Unauthorized when no credentials
        are provided.
        """
        self.client.credentials()
        self.url = reverse(
            'reviews-detail', kwargs={'review_id': self.review.id})
        data = {"rating": 5, "description": "Noch besser als erwartet!"}
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_reviews_return_403(self):
        """
        Ensure a consumer is completely blocked from tampering with somebody
        else's review record.
        """
        self.url = reverse(
            'reviews-detail', kwargs={'review_id': self.review.id})
        self.token = Token.objects.create(user=self.customer_user2)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        data = {"rating": 5, "description": "Noch besser als erwartet!"}
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_reviews_return_404(self):
        """
        Ensure update attempts on non-existent review tracking primary keys
        report a 404 Not Found.
        """
        self.url = reverse('reviews-detail', kwargs={'review_id': 9999})
        data = {"rating": 5, "description": "Test"}
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_reviews_return_401(self):
        """
        Ensure anonymous deletion executions are dropped immediately with a
        401 Unauthorized status.
        """
        self.client.credentials()
        self.url = reverse(
            'reviews-detail', kwargs={'review_id': self.review.id})
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_reviews_wrong_user_return_403(self):
        """
        Ensure alternative users lack permissions to wipe third-party review
        records from the database.
        """
        self.url = reverse(
            'reviews-detail', kwargs={'review_id': self.review.id})
        self.token = Token.objects.create(user=self.customer_user2)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_non_existing_reviews_return_404(self):
        """
        Ensure system safely returns a 404 Not Found during removal setups on
        missing entity records.
        """
        self.url = reverse('reviews-detail', kwargs={'review_id': 9999})
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
