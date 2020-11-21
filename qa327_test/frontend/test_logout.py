import pytest
from seleniumbase import BaseCase

from qa327_test.conftest import base_url
from unittest.mock import patch
from qa327.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

test_user = User(
    email='test_frontend@test.com',
    name='test_frontend',
    password=generate_password_hash('Testfrontend123!'),
    balance=5000
)

class FrontEndLogoutTesting(BaseCase):
    @patch('qa327.backend.get_user', return_value=test_user)
    def login(self, *_):
        self.open(base_url + '/login')
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Testfrontend123!")
        self.click('input[type="submit"]')

        # open home page
        self.open(base_url)

    # Test Case R7 - Logout will invalid the current session and redirect to the login page. 
    #                  After logout, the user shouldn't be able to access restricted pages.
    def test_logout(self):
        # test if the page loads correctly
        self.login()
        self.click_link_text('logout')
        # try to open homepage
        self.open(base_url + '/')
        # verify on login page
        self.assert_element('#message')
        self.assert_text('Please login', '#message')
        