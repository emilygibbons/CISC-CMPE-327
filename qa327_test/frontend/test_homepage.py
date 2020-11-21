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
    {'name': 't1', 'price': 100, 'email': 'test_frontend@test.com', 'date': '20200901'}
]


class FrontEndHomePageTesting(BaseCase):

    # Test case for R.3.7
    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_contains_buy_field(self, *_):

        self.open(base_url + '/login')
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Testfrontend123!")
        self.click('input[type="submit"]')

        # open home page

        self.open(base_url)

        # test if buy field is loaded on page

        self.assert_text("Buy now!", "#buy-header")
        self.assert_element("#buy-form")
        self.assert_element("#buy-quantity")
        self.assert_element("#buy-name")

    # Need this whenever the home page is accessed. Will need to add more when /buy,etc is acccessed.
    # Testing for R.3.8
    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_contains_update_field(self, *_):
           
        self.open(base_url + '/login')
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Testfrontend123!")
        self.click('input[type="submit"]')

        # open home page
        self.open(base_url)

        #Test if update-header loaded corredtly 

        self.assert_text("Update a current listing.", "#update-header")
        self.assert_element("#update-form")
        self.assert_element("#quantity-old")
        self.assert_element("#name-old")
        self.assert_element("#price-old")
        self.assert_element("#expiration-date-old")

        self.assert_element("#quantity-new")
        self.assert_element("#name-new")
        self.assert_element("#price-new")
        self.assert_element("#expiration-date-new")

    # Testing for R.3.9
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

        # check if sell can be posted

        self.type("#sell-quantity", "1")
        self.type("#sell-name", "t2")
        self.type("#sell-price", "100")
        self.type("#sell-expiration-date", "20200902")
        self.click('input[id="btn-sell-submit"]')

        # Assert page is redirected to '/' implies posted to /sell.
        self.assert_element("#welcome-header")
        self.assert_text("Welcome test_frontend", "#welcome-header")
        self.assert_element("#tickets-header")
        # ticket formatL Quantity: 1 Owner's email: Price: $100 Expiration Date: Ticket name: t1

        self.assert_text(
            "Quantity: 1 Owner's email: test_frontend@test.com Price: $100 Expiration Date: 20200901 Ticket name: t1", "#tickets-header")

    # Testing for R.3.10
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

        # check if buy can be posted

        self.type("#buy-quantity", "1")
        self.type("#buy-name", "t2")
        self.click('input[id="btn-buy-submit"]')

        # Assert page is redirected to '/' assuring that it was posted to /buy.

        self.assert_element("#welcome-header")
        self.assert_text("Welcome test_frontend", "#welcome-header")
        self.assert_element("#tickets-header")
        # ticket formatL Quantity: 1 Owner's email: Price: $100 Expiration Date: Ticket name: t1

        self.assert_text(
            "Quantity: 1 Owner's email: test_frontend@test.com Price: $100 Expiration Date: 20200901 Ticket name: t1", "#tickets-header")

    # Testing for R.3.11
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

    # Test Case R3.1 - If the user hasn't logged in, show the login page
    def test_forced_loginpage(self):
        # open homepage for it to redirect to /login
        self.open(base_url + '/')
        # give it one second to redirect
        self.wait(1)
        # make sure it shows the login page
        self.assert_element('#message')
        self.assert_text('Please login', '#message')

    # Test Case R3.2 - The page shows a header 'Welcome (user.name)'
    def test_welcomemessage(self):
        # log in test user
        self.login()
        # verify welcome message shown with user's name attached
        self.assert_element("#welcome-header")
        self.assert_text("Welcome test_frontend!", "#welcome-header")

    # Test Case R3.3 - The page shows user balance
    def test_userbalance(self):
        # log in test user
        self.login()
        # verify balance is shown 
        self.assert_element("#balance-paragraph")
        self.assert_text("Balance: $" + str(test_user.balance),
                         '#balance-paragraph') 

    # Test Case R3.4 - The page shows a logout link, pointing to /logout
    def test_logout(self):
        # log in test user
        self.login()
        # logout user
        self.click_link_text('logout')
        # verify redirected to login page
        self.assert_element('#message')
        self.assert_text('Please login', '#message')

    # Test Case R3.5 - The page lists all available tickets, including quantity, owner's email, and the price, for unexpired tickets
    @patch('qa327.backend.get_all_tickets', return_value= test_tickets)
    @patch('qa327.backend.get_user', return_value= test_user)
    def test_ticketdisplay(self, *_):
        # login as test user
        self.login()
        # verify on homepage
        self.assert_element("#tickets-header")
       
        self.assert_text("Quantity: 1 Owner's email: test_frontend@test.com Price: $100 Expiration Date: 20200901 Ticket name: t1", "#tickets-header")
       
                        
    # Test Case R3.6 - The page contains a form that a user can submit new tickets to sell. Fields:name, quantity, price, expiration date
    def test_sellform(self):
        # login as test user
        self.login()
        # verify all attributes of tickets are shown on form
        self.assert_element('#sell-quantity')
        self.assert_element('#sell-name')
        self.assert_element('#sell-price')
        self.assert_element('#sell-expiration-date')
        self.type("#quantity-old", "1")
        self.type("#name-old", "t2")
        self.type("#price-old", "100")
        self.type("#expiration-date-old", "20200902")
        self.type("#quantity-new", "1")
        self.type("#name-new", "t3")
        self.type("#price-new", "101")
        self.type("#expiration-date-new", "20200903")
        self.click('input[id="btn-update-submit"]')

        # Assert page is redirected to '/' assuring it was posted to /update.
        self.assert_element("#welcome-header")
        self.assert_text("Welcome test_frontend", "#welcome-header")
        self.assert_element("#tickets-header")
        # ticket formatL Quantity: 1 Owner's email: Price: $100 Expiration Date: Ticket name: t1

        self.assert_text(
            "Quantity: 1 Owner's email: test_frontend@test.com Price: $100 Expiration Date: 20200901 Ticket name: t1", "#tickets-header")
