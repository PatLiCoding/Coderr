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
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_get_response(self):
    #     response = self.client.get(self.url)
    #     print(response.data)
    #     assert False
