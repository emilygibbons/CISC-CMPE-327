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


# test from start to finish that a user can register, login, and buy a ticket, then logout
@pytest.mark.usefixtures('server')
class BuyTicket(BaseCase):
    def login(self):
        # Login to Swag Labs and verify that login was successful.
        self.open(base_url + '/login')
        self.type("#email", "test1@gmail.com")
        self.type("#password", "Testing123!")
        self.click('input[type="submit"]')

    def buy(self):
        # buy a ticket
        self.type("#buy-quantity", "1")
        self.type("#buy-name", "testingASale")
        self.click('input[id="btn-buy-submit"]')

    def test_buy(self):
        #attempt to buy a ticket and confirm it was successful
        self.login()
        self.buy()
        self.assert_element("#buyMessage")
        self.assert_text(
            "Purchase successful", "#buyMessage")
        self.click_link_text('logout')
        self.assert_element('#message')
        self.assert_text('Please login', '#message')