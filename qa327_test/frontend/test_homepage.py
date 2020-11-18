import pytest
from seleniumbase import BaseCase

from qa327_test.conftest import base_url
from unittest.mock import patch
from qa327.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

"""
This file defines all unit tests for the frontend homepage.

The tests will only test the frontend portion of the program, by patching the backend to return
specfic values. For example:

@patch('qa327.backend.get_user', return_value=test_user)

Will patch the backend get_user function (within the scope of the current test case)
so that it return 'test_user' instance below rather than reading
the user from the database.

Annotate @patch before unit tests can mock backend methods (for that testing function)
"""


# Mock a sample user

test_user = User(
    email='test_frontend@test.com',
    name='test_frontend',
    password=generate_password_hash('Testfrontend123!'),
    balance=5000

)

# Mock some sample tickets

test_tickets = [
    {'name': 't1', 'price': '100', 'email': 'test_frontend@test.com', 'date': '20200901'}
]


class FrontEndHomePageTesting(BaseCase):

    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_contains_buy_field(self, *_):

        self.open(base_url + '/login')
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Testfrontend123!")
        self.click('input[type="submit"]')

        # open home page

        self.open(base_url)
        # test if the page loads correctly

        self.assert_element("#welcome-header")
        self.assert_text("Welcome test_frontend", "#welcome-header")
        self.assert_element("#tickets-header")

        # ticket formatL Quantity: 1 Owner's email: Price: $100 Expiration Date: Ticket name: t1

        self.assert_text(
            "Quantity: 1 Owner's email: test_frontend@test.com Price: $100 Expiration Date: 20200901 Ticket name: t1", "#tickets-header")

        # test if buy field is loaded on page

        self.assert_text("Buy now!", "#buy-header")
        self.assert_element("#buy-form")

    # Need this whenever the home page is accessed. Will need to add more when /buy,etc is acccessed.

    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_contains_update_field(self, *_):
           
        self.open(base_url + '/login')
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Testfrontend123!")
        self.click('input[type="submit"]')

        # open home page
        self.open(base_url)
        # test if the page loads correctly
        self.assert_element("#welcome-header")
        self.assert_text("Welcome test_frontend", "#welcome-header")
        self.assert_element("#tickets-header")
        # ticket formatL Quantity: 1 Owner's email: Price: $100 Expiration Date: Ticket name: t1

        self.assert_text(
            "Quantity: 1 Owner's email: test_frontend@test.com Price: $100 Expiration Date: 20200901 Ticket name: t1", "#tickets-header")

        #test if the update field is there.

        self.assert_text("Update a current listing.", "#update-header")
        self.assert_element("#update-form")

    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    @patch('qa327.backend.sell_ticket', return_value=True)
    def test_posted_sell(self, *_):
        self.open(base_url + '/login')
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Testfrontend123!")
        self.click('input[type="submit"]')

        # open home page
        self.open(base_url)
        # test if the page loads correctly
        self.assert_element("#welcome-header")
        self.assert_text("Welcome test_frontend", "#welcome-header")
        self.assert_element("#tickets-header")
        # ticket formatL Quantity: 1 Owner's email: Price: $100 Expiration Date: Ticket name: t1

        self.assert_text(
            "Quantity: 1 Owner's email: test_frontend@test.com Price: $100 Expiration Date: 20200901 Ticket name: t1", "#tickets-header")

        # check if sell can be posted

        self.type("#sell-quantity", "1")
        self.type("#sell-name", "t2")
        self.type("#sell-price", "100")
        self.type("#sell-expiration-date", "20200902")
        self.click('input[id="btn-sell-submit"]')

        # Assert page is redirected to '/'.
        self.assert_element("#welcome-header")
        self.assert_text("Welcome test_frontend", "#welcome-header")
        self.assert_element("#tickets-header")
        # ticket formatL Quantity: 1 Owner's email: Price: $100 Expiration Date: Ticket name: t1

        self.assert_text(
            "Quantity: 1 Owner's email: test_frontend@test.com Price: $100 Expiration Date: 20200901 Ticket name: t1", "#tickets-header")

    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    @patch('qa327.backend.buy_ticket', return_value=True)
    def test_posted_buy(self, *_):
        self.open(base_url + '/login')
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Testfrontend123!")
        self.click('input[type="submit"]')

        # open home page
        self.open(base_url)
        # test if the page loads correctly
        self.assert_element("#welcome-header")
        self.assert_text("Welcome test_frontend", "#welcome-header")
        self.assert_element("#tickets-header")
        # ticket formatL Quantity: 1 Owner's email: Price: $100 Expiration Date: Ticket name: t1

        self.assert_text(
            "Quantity: 1 Owner's email: test_frontend@test.com Price: $100 Expiration Date: 20200901 Ticket name: t1", "#tickets-header")

        # check if buy can be posted

        self.type("#buy-quantity", "1")
        self.type("#buy-name", "t2")
        self.click('input[id="btn-buy-submit"]')

        # Assert page is redirected to '/'.
        self.assert_element("#welcome-header")
        self.assert_text("Welcome test_frontend", "#welcome-header")
        self.assert_element("#tickets-header")
        # ticket formatL Quantity: 1 Owner's email: Price: $100 Expiration Date: Ticket name: t1

        self.assert_text(
            "Quantity: 1 Owner's email: test_frontend@test.com Price: $100 Expiration Date: 20200901 Ticket name: t1", "#tickets-header")

    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    @patch('qa327.backend.delete_ticket', return_value=True)
    @patch('qa327.backend.sell_ticket', return_value=True)
    def test_update_form(self,*_):
        self.open(base_url + '/login')
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Testfrontend123!")
        self.click('input[type="submit"]')

        # open home page
        self.open(base_url)
        # test if the page loads correctly
        self.assert_element("#welcome-header")
        self.assert_text("Welcome test_frontend", "#welcome-header")
        self.assert_element("#tickets-header")
        # ticket formatL Quantity: 1 Owner's email: Price: $100 Expiration Date: Ticket name: t1

        self.assert_text(
            "Quantity: 1 Owner's email: test_frontend@test.com Price: $100 Expiration Date: 20200901 Ticket name: t1", "#tickets-header")

        # check if update can be posted

        self.type("#quantity-old", "1")
        self.type("#name-old", "t2")
        self.type("#price-old", "100")
        self.type("#expiration-date-old", "20200902")
        self.type("#quantity-new", "1")
        self.type("#name-new", "t3")
        self.type("#price-new", "101")
        self.type("#expiration-date-new", "20200903")
        self.click('input[id="btn-update-submit"]')

        # Assert page is redirected to '/'.
        self.assert_element("#welcome-header")
        self.assert_text("Welcome test_frontend", "#welcome-header")
        self.assert_element("#tickets-header")
        # ticket formatL Quantity: 1 Owner's email: Price: $100 Expiration Date: Ticket name: t1

        self.assert_text(
            "Quantity: 1 Owner's email: test_frontend@test.com Price: $100 Expiration Date: 20200901 Ticket name: t1", "#tickets-header")