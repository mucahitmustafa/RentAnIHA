from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class LoginTestCase(TestCase):
    def setUp(self):
        self.login_url = reverse('login')
        self.signup_url = reverse('signup')
        self.user = User.objects.create_user(username='userForTesting', password='Password1ForTesting',
                                             email='mailForTesting@gmail.com')

    def test_login_page_should_return_200_status_code(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)

    def test_user_login_with_correct_credentials_should_login_successfully(self):
        login_data = {
            'username': 'userForTesting',
            'password': 'Password1ForTesting'
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_user_login_with_invalid_credentials_should_stay_on_login_page(self):
        login_data = {
            'username': 'userForTesting',
            'password': 'WrongPassword'
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)
