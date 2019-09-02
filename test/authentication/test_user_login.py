from test.base import BaseTestCase
from api_v1.models.user import User


class UserAuthentication(BaseTestCase):
    """
    Class to test for user authentication.
    """

    def setUp(self):
        super().setUp()
        self.login_user = self.client.post(
            '/api/v1/register/', self.register)
        self.login = {
            "username": self.register['username'],
            "password": self.register['password']
        }
        self.user = User.objects.get(username=self.register['username'])
        self.user.active = True
        self.user.save()

    def test_user_login(self):
        # Check if test user exists in the database

        response = self.client.post(
            '/api/v1/login/', self.login)
        self.assertEqual(response.status_code, 200)

    def test_unverfied_login(self):
        # Check if test user exists in the database
        self.user.active = False
        self.user.save()
        response = self.client.post(
            '/api/v1/login/', self.login)
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            'Inactive account, check your mail to activate your account',
            response.data['error'])

    def test_incorrect_email_login(self):
        # Test if the user can log in with an incorrect username.
        self.login['username'] = 'username'
        response = self.client.post(
            '/api/v1/login/', self.login)
        data = response.data
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            'Invalid username/password', data['error'])

    def test_incorrect_password_login(self):
        # Test if the user can log in with a wrong password.
        self.login['password'] = 'password'
        response = self.client.post(
            '/api/v1/login/', self.login)
        data = response.data
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            'Invalid username/password', data['error'])

    def test_invalid_data(self):
        # Test if the user sends an invalid data
        response = self.client.post(
            '/api/v1/login/')
        data = response.data
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            'Please provide username/password', data['error'])
