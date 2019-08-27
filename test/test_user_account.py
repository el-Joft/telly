from .base import BaseTestCase


class UserAccount(BaseTestCase):

    def test_creating_user(self):
        """Test post activities in the database."""
        self.user_data['email'] = 'newemail@gmail.com'
        self.user_data['mobile_number'] = '+2348136681135'
        response = self.client.post(
            '/api/v1/register/', self.user_data)
        data = response.data["data"]
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(data['email'], 'newemail@gmail.com')

    def test_existing_user(self):
        """ Test if user details exist in the database"""
        self.user_data['mobile_number'] = '+2348136681132'
        response = self.client.post(
            '/api/v1/register/', self.user_data)
        data = response.data
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['status'], 'error')
        self.assertIn(
            'User with this email already exists.', data['data']['email'])

    def test_invalid_password(self):
        """ Test if user details exist in the database"""
        self.user_data['email'] = 'passwordemail@gmail.com'
        self.user_data['mobile_number'] = '+2348136681133'
        self.user_data['password'] = '1234'
        response = self.client.post(
            '/api/v1/register/', self.user_data)
        data = response.data
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['status'], 'error')
        self.assertIn(
            'Password must contain a Number, a letter and 8 charcters long',
            data['data']['non_field_errors'])
