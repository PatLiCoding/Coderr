from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import default_storage
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
            last_name='lastname'
        )
        self.profile = Profile.objects.create(
            user=self.user,
            file="profile_picture.jpg",
            tel="123456789",
            location="Berlin",
            description="Business description",
            working_hours="9-17",
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.url = reverse('profile', kwargs={'user_id': self.user.id})

    def tearDown(self):
        """
        Ensures that files created during the test are deleted.
        """
        custom_path = f'uploads/user_{self.user.id}/profile.jpg'
        if default_storage.exists(custom_path):
            default_storage.delete(custom_path)

    def test_get_profil_by_id(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_profile_data_and_file(self):
        """
        Tests the successful updating of profile and user data, as well as
        a file.
        """
        dummy_file = SimpleUploadedFile(
            name="new_avatar.jpg",
            content=b"file_content_here",
            content_type="image/jpeg"
        )
        data = {
            'first_name': 'Maurice',
            'last_name': 'Mustermann',
            'location': 'Köln',
            'tel': '987654321',
            'email': 'Brenda_Reichel@gmail.com',
            'file': dummy_file
        }
        response = self.client.patch(self.url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Maurice')
        self.assertEqual(self.user.last_name, 'Mustermann')
        self.assertEqual(self.user.email, 'Brenda_Reichel@gmail.com')
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.location, 'Köln')
        self.assertEqual(self.profile.tel, '987654321')
        expected_file_path = f'uploads/user_{self.user.id}/profile.jpg'
        self.assertEqual(self.profile.file.name, expected_file_path)
        self.assertTrue(default_storage.exists(expected_file_path))
