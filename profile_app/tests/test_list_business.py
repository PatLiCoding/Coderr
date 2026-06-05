from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from auth_app.models import User
from profile_app.models import Profile


class ProfilTestsHappyPath(APITestCase):
    """
    Test cases for successful API requests (Happy Path) regarding
    business profiles.
    """

    def setUp(self):
        """
        Set up the test environment: create a business user,
        an associated profile, and authenticate the client using a token.
        """
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123',
            first_name='firstname',
            last_name='lastname',
            type='business'
        )
        self.profile = Profile.objects.create(
            user=self.user,
            tel="123456789",
            location="Berlin",
            description="Business description",
            working_hours="9-17",
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.url = reverse('business')

    def test_get_list_business_return_200(self):
        """
        Ensure an authenticated business user can successfully retrieve the
        list (status 200).
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProfilTestsUnhappyPath(APITestCase):
    """
    Test cases for failed or unauthorized API requests (Unhappy Path)
    regarding business profiles.
    """

    def setUp(self):
        """
        Set up the test environment for failure scenarios (without automatic
        client authentication).
        """
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123',
            first_name='firstname',
            last_name='lastname',
            type='business'
        )
        self.profile = Profile.objects.create(
            user=self.user,
            tel="123456789",
            location="Berlin",
            description="Business description",
            working_hours="9-17",
        )
        self.url = reverse('business')

    def test_get_list_business_unauthenticated_returns_401(self):
        """
        Failure: The user is not logged in (no token provided in the header).
        """
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
