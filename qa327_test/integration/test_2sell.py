import pytest
from seleniumbase import BaseCase
from qa327.models import db, User
from qa327_test.conftest import base_url
from werkzeug.security import generate_password_hash, check_password_hash


# integration testing: the test case interacts with the
# browser, and test the whole system (frontend+backend).
@pytest.mark.usefixtures('server')
class ListTicket(BaseCase):

    def login(self):
        # Login to Swag Labs and verify that login was successful.

        self.open(base_url + '/login')
        self.type("#email", "test1@gmail.com")
        self.type("#password", "Testing123!")
        self.click('input[type="submit"]')

    def sell(self):
        # sell a ticket and verify that the ticket appears at the top of the page
        self.type("#sell-quantity", "1")
        self.type("#sell-name", "testingASale")
        self.type("#sell-price", "85")
        self.type("#sell-expiration-date", "20250325")
        self.click('input[id="btn-sell-submit"]')

    def test_sell(self):
        # attempt to sell a ticket and confirm that the ticket is posted to the page.
        self.login()
        self.sell()
        self.assert_element("#tickets-header")
        self.assert_text(
            "Quantity: 1 Owner's email: test1@gmail.com Price: $85 Expiration Date: 20250325 Ticket name: testingASale", "#tickets-header")
        self.click_link_text('logout')
        self.assert_element('#message')
        self.assert_text('Please login', '#message')
