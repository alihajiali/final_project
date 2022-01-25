from urllib import response
from django.test import SimpleTestCase, TestCase, Client
from ...models import User, Profile
from django.urls import reverse, resolve
from .views import (
    RegisterView, 
    ShowProfileView, 
    CreateProfileView
)

# python manage.py test accounts.api.v1.tests

class TestUrls(SimpleTestCase):
    def test_token(self):
        url = reverse("api_accounts:register")
        self.assertEqual(resolve(url).func.view_class, RegisterView)

    def test_profile(self):
        url = reverse('api_accounts:profile', args=['test_username'])
        self.assertEqual(resolve(url).func.view_class, ShowProfileView)

    # def test_