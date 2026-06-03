from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from auth_app.models import User
from profile_app.models import Profile


class ProfilTestsHappyPath(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123'
        )
        self.profile = Profile.objects.create(
            user=self.user,
            file="profile_picture.jpg",
            tel="123456789",
            location="Berlin",
            description="Business description",
            working_hours="9-17",
            email="max@business.de",
            created_at="2023-01-01T12:00:00Z"
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get_profil_by_id(self):
        url = reverse('profile', kwargs={'user_id': self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
