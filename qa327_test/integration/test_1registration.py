import pytest
from seleniumbase import BaseCase
from qa327.models import db, User
from qa327_test.conftest import base_url
from werkzeug.security import generate_password_hash, check_password_hash


# integration testing: the test case interacts with the
# browser, and test the whole system (frontend+backend).

test_user = User(
    email='test_frontend@test.com',
    name='test_frontend',
    password=generate_password_hash('Testfrontend123!'),
    balance=5000
)


@pytest.mark.usefixtures('server')
class Registered(BaseCase):

    def register(self):
        # register new user

        self.open(base_url + '/register')
        self.type("#email", "test1@gmail.com")
        self.type("#name", "test1")
        self.type("#password", "Testing123!")
        self.type("#password2", "Testing123!")
        self.click('input[type="submit"]')

    def login(self):
        # Login to Swag Labs and verify that login was successful.

        self.open(base_url + '/login')
        self.type("#email", "test1@gmail.com")
        self.type("#password", "Testing123!")
        self.click('input[type="submit"]')

    def test_register_login(self):
        # This test checks the implemented login/logout feature
        self.register()
        self.login()
        # self.open(base_url)
        self.assert_element("#welcome-header")
        self.assert_text("Welcome test1", "#welcome-header")

    def test_no_duplicate_users(self):
        self.register()
        self.register()
        self.assert_element("#message")
        self.assert_text("this email has been ALREADY used", "#message")


