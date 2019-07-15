from django.test import Client, TestCase
from api_v1.models import User
from api_v1.models import Role


class BaseTestCase(TestCase):
    """
    Base configuration file for all tests.
    """

    @classmethod
    def setUpClass(cls):

        # We need to first run setUpClass function that we
        # inherited from TestCase.
        super(BaseTestCase, cls).setUpClass()

        # Set up test client for all test classes
        # that will inherit from this class.
        cls.client = Client()

    def setUp(self):
        """
        Configurations to be made available before each
        individual test case inheriting from this class.
        """
        self.role = Role.objects.create(role_type='User')
        self.user_data = {
            "first_name": "Firstname",
            "password": "123456ABC",
            "last_name": "lastname",
            "username": "test",
            "mobile_number": "+2348136681130",
            "email": "test1@gmail.com",
            "role_id": self.role.id
        }
        self.user_data_2 = {
            "first_name": "Firstname",
            "password": "123456ABC",
            "last_name": "lastname",
            "mobile_number": "+2348136681131",
            "username": "test",
            "email": "test2@gmail.com",
            "role_id": self.role.id
        }

        self.new_user = User(**self.user_data)

        self.new_user_2 = User(**self.user_data_2)

        self.new_user.save()
