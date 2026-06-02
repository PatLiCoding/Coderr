from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from auth_app.models import User


class AuthTestsHappyPath(APITestCase):

    def setUp(self):
        """
        Set up response data and test users for happy path scenarios.
        """
        self.registration_data = {
            "username": "exampleUsername",
            "email": "example@mail.de",
            "password": "examplePassword",
            "repeated_password": "examplePassword",
            "type": "customer",
        }
        self.existing_user = User.objects.create_user(
            username="loginUser",
            email="login@mail.de",
            password="secretPassword",
            type="customer",
        )
        self.login_data = {
            "username": "loginUser",
            "password": "secretPassword"
        }

    def test_post_registration(self):
        """
        Test successful user registration:
        - Verify 201 Created status code.
        - Verify valid registration data and response structure (
            token, username, email, user_id).
        - Confirm the newly created user exists in the database.
        """
        url = reverse('registration')
        response = self.client.post(url, self.registration_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['username'],
                         self.registration_data['username'])
        self.assertEqual(response.data['email'],
                         self.registration_data['email'])
        self.assertIn('user_id', response.data)
        self.assertTrue(User.objects.filter(
            username="exampleUsername").exists())

    def test_post_login(self):
        """
        Test successful user login:
        - Verify 200 OK status code on correct credentials.
        - Verify the API returns an authentication token.
        - Verify the returned username matches.
        """
        url = reverse('login')
        response = self.client.post(url, self.login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['username'],
                         self.login_data['username'])


class AuthTestsUnhappyPath(APITestCase):

    def setUp(self):
        """
        Set up test data and existing users for error and validation scenarios.
        """
        self.registration_data = {
            "username": "unhappyUser",
            "email": "unhappy@mail.de",
            "password": "securePassword123",
            "repeated_password": "securePassword123",
            "type": "customer",
        }
        self.existing_user = User.objects.create_user(
            username="existingUser",
            email="existing@mail.de",
            password="correctPassword",
            type="customer",
        )

    def test_registration_passwords_do_not_match(self):
        """
        Test that registration fails when password and repeated_password
        do not match (400 Bad Request).
        Ensures the user is not created in the database.
        """
        url = reverse('registration')
        bad_data = self.registration_data.copy()
        bad_data['repeated_password'] = 'wrongRepeatedPassword'
        response = self.client.post(url, bad_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(User.objects.filter(username="unhappyUser").exists())

    def test_registration_username_already_exists(self):
        """
        Test that registration fails when the username is already taken
        (400 Bad Request).
        """
        url = reverse('registration')
        bad_data = self.registration_data.copy()
        bad_data['username'] = 'existingUser'
        response = self.client.post(url, bad_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_missing_fields(self):
        """
        Test that registration fails when required fields (like email)
        are missing or null (400 Bad Request).
        """
        url = reverse('registration')
        bad_data = self.registration_data.copy()
        bad_data['email'] = None
        response = self.client.post(url, bad_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_wrong_password(self):
        """
        Test that login fails when providing an incorrect password.
        Expects a 400 Bad Request (or 401 Unauthorized depending on DRF config)
        and no token in response.
        """
        url = reverse('login')
        wrong_login_data = {
            "username": "existingUser",
            "password": "wrongPassword123"
        }
        response = self.client.post(url, wrong_login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)

    def test_login_non_existing_user(self):
        """
        Test that login fails when the user does not exist in the database.
        Expects a 400 Bad Request (or 401 Unauthorized) and no token in
        response.
        """
        url = reverse('login')
        wrong_login_data = {
            "username": "doesNotExist",
            "password": "somePassword"
        }
        response = self.client.post(url, wrong_login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)
