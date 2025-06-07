from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import date

User = get_user_model()

class CustomUserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='password123',
            bio='Esta es una bio de prueba.',
            birth_date=date(1990, 1, 1),
            country='US',
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.bio, 'Esta es una bio de prueba.')
        self.assertEqual(self.user.birth_date, date(1990, 1, 1))
        self.assertEqual(self.user.country.code, 'US')
        self.assertEqual(str(self.user), 'testuser')

    def test_profile_picture_upload(self):
        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'\x47\x49\x46\x38\x89\x61\x00\x00',
            content_type='image/jpeg'
        )
        user_with_pic = User.objects.create_user(
            username='userpic',
            password='password123',
            profile_picture=image
        )
        self.assertTrue(user_with_pic.profile_picture.name.startswith('profiles/test_image'))

class CustomUserViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_login(self):
        login = self.client.login(username='testuser', password='password123')
        self.assertTrue(login)

