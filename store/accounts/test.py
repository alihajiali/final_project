from urllib import response
from django.test import SimpleTestCase, TestCase, Client
from .models import User, Profile
from django.urls import reverse, resolve
from .views import (
    login, 
    register, 
    log_out, 
    profile, 
    EditProfile, 
    CreateShop, 
    EditShop, 
    DeleteShop
)
from .forms import (
    SignUpForm, 
    ProfileUserForm, 
    NewMarket
)
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

# run test : python manage.py test accounts

class TestUrls(SimpleTestCase):
    def test_login(self):
        url = reverse('accounts:login')
        self.assertEqual(resolve(url).func.view_class, login)

    def test_register(self):
        url = reverse('accounts:register')
        self.assertEqual(resolve(url).func.view_class, register)

    def test_log_out(self):
        url = reverse('accounts:log_out')
        self.assertEqual(resolve(url).func.view_class, log_out)

    def test_profile(self):
        url = reverse('accounts:profile')
        self.assertEqual(resolve(url).func.view_class, profile)

    def test_EditProfile(self):
        url = reverse('accounts:edit_profile')
        self.assertEqual(resolve(url).func.view_class, EditProfile)

    def test_CreateShop(self):
        url = reverse('accounts:create_market')
        self.assertEqual(resolve(url).func.view_class, CreateShop)

    def test_EditShop(self):
        url = reverse('accounts:edit_market', args=['shop_name'])
        self.assertEqual(resolve(url).func.view_class, EditShop)

    def test_DeleteShop(self):
        url = reverse('accounts:delete_market', args=['shop_name'])
        self.assertEqual(resolve(url).func.view_class, DeleteShop)


# -----------------------------------------------------------------


class TestSignUpForm(TestCase):
    def test_valid_data(self):
        form = SignUpForm(data={'full_name':'test', 'email':'test@test.test', 'password1':'Test1234', 'password2':'Test1234'})
        self.assertTrue(form.is_valid())

    def test_invalid_data(self):
        form = SignUpForm(data = {})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)




class TestProfileUserForm(TestCase):
    def test_invalid_data(self):
        form = ProfileUserForm(data = {})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)




class TestNewMarket(TestCase):
    def test_valid_data(self):
        form = NewMarket(data={'title':'test', 'slug':'test', 'owner':'test', 'status':'P', 'type':'S'})
        self.assertTrue(form.is_valid())

    def test_invalid_data(self):
        form = NewMarket(data = {})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)


# -------------------------------------------------------------


class TestUserModel(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@test.test', full_name='test', password='Test1234')

    def test_is_admin(self):
        self.assertFalse(self.user.is_admin)

    def test_is_active(self):
        self.assertTrue(self.user.is_active)

    def test_is_seller(self):
        self.assertFalse(self.user.is_seller)


# ----------------------------------------------------------



class TestLoginView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_user_login_view_Get(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_user_login_view_Post_valid_data(self):
        response = self.client.post(reverse('accounts:login'), data={
            'email':'test@test.test', 
            'password':'Test1234'
        })
        self.assertEqual(response.status_code, 200)
    
    def test_user_login_view_Post_invalid_data(self):
        response = self.client.post(reverse('accounts:login'), data={
            'email':'', 
            'password':''
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['form'].errors), 2)




class TestRegisterView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_user_register_view_Get(self):
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')
        self.failUnless(response.context['form'], SignUpForm)

    def test_user_register_view_Post_valid_data(self):
        response = self.client.post(reverse('accounts:register'), data={
            'full_name':'test', 
            'email':'test@test.test', 
            'password1':'Test1234', 
            'password2':'Test1234'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounts:login'))
        self.assertEqual(User.objects.count(), 1)

    def test_user_register_view_Post_invalid_data(self):
        response = self.client.post(reverse('accounts:register'), data={
            'full_name':'', 
            'email':'', 
            'password1':'', 
            'password2':''
        })
        self.failIf(response.context['form'].is_valid())
        self.assertEqual(len(response.context['form'].errors), 3)
        self.assertEqual(response.status_code ,200)



class TestLogOut(TestCase):
    def setUp(self):
        self.client = Client()

    def test_log_out_Get(self):
        response = self.client.get(reverse('accounts:log_out'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('shop:home'))




class TestProfile(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_profile_view_Get(self):
        response = self.client.get(reverse('accounts:profile'))
        self.client.login(email='test@test.test', password='Test1234')
        self.assertEqual(response.status_code, 302)
