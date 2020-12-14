import pytest
from seleniumbase import BaseCase

from qa327_test.conftest import base_url
from unittest.mock import patch
from qa327.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

"""
This file defines all unit tests for the frontend sell section.

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
    {'name': 'ticket1', 'price': 100, 'email': 'test_frontend@test.com', 'date': '20210901'}
]


class FrontEndSellTesting(BaseCase):
    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def login(self, *_):
        self.open(base_url + '/login')
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Testfrontend123!")
        self.click('input[type="submit"]')

        # open home page
        self.open(base_url)

    # Test Case R4.1 - The name of the ticket has to be alphanumeric-only, and space allowed only if it is not the first or the last character.
    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_ticketname(self,*_):
        # login as test user
        self.login()
        # Positive case is covered under test R4.7

        # NEGATIVE: IF IT HAS A SYMBOL
        # fill in ticket information 
        self.type("#sell-quantity","1")
        self.type("#sell-name","ticket1!")
        self.type("#sell-price","100")
        self.type("#sell-expiration-date","20210901")
        # click sell button
        self.click('input[id="btn-sell-submit"]')
        # make sure it gives proper error message
        self.assert_element("#sellMessage")
        self.assert_text("The name has to alphanumeric, have no spaces in the beginning or end and be between 6 and 60 characters.", "#sellMessage")

        # NEGATIVE: IF IT STARTS WITH A SPACE
        # fill in ticket information
        self.type("#sell-quantity","1")
        self.type("#sell-name"," ticket1")
        self.type("#sell-price","100")
        self.type("#sell-expiration-date","20210901")
        # click sell button
        self.click('input[id="btn-sell-submit"]')
        # make sure it gives proper error message
        self.assert_element("#sellMessage")
        self.assert_text("The name has to alphanumeric, have no spaces in the beginning or end and be between 6 and 60 characters.", "#sellMessage")

        # NEGATIVE: IF IT ENDS WITH A SPACE
        # fill in ticket information
        self.type("#sell-quantity","1")
        self.type("#sell-name"," ticket1 ")
        self.type("#sell-price","100")
        self.type("#sell-expiration-date","20210901")
        # click sell button
        self.click('input[id="btn-sell-submit"]')
        # make sure it gives proper error message
        self.assert_element("#sellMessage")
        self.assert_text("The name has to alphanumeric, have no spaces in the beginning or end and be between 6 and 60 characters.", "#sellMessage")

    # Test Case R4.2 and R4.8 -The name of the ticket is no longer than 60 characters and more than 6 characters.
    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_ticketlength(self,*_):
        # login as test user
        self.login()
        # Positive case is covered under test R4.7

        # NEGATIVE: MORE THAN 60 CHARACTERS
        # fill in ticket information
        self.type("#sell-quantity","1")
        self.type("#sell-name","qqqwwweeerrrtttyyyuuuiiiooopppaaasssdddfffggghhhjjjkkkllzzzxxxx")
        self.type("#sell-price","100")
        self.type("#sell-expiration-date","20210901")
        # click sell button
        self.click('input[id="btn-sell-submit"]')
        # make sure it gives proper error message
        self.assert_element("#sellMessage")
        self.assert_text("The name has to alphanumeric, have no spaces in the beginning or end and be between 6 and 60 characters.", "#sellMessage")

        # NEGATIVE: LESS THAN 6 CHARACTERS
        # fill in ticket information
        self.type("#sell-quantity","1")
        self.type("#sell-name","t2")
        self.type("#sell-price","100")
        self.type("#sell-expiration-date","20210901")
        # click sell button
        self.click('input[id="btn-sell-submit"]')
        # make sure it gives proper error message
        self.assert_element("#sellMessage")
        self.assert_text("The name has to alphanumeric, have no spaces in the beginning or end and be between 6 and 60 characters.", "#sellMessage")

    # Test Case R4.3 - The quantity of the tickets has to be more than 0, and less than or equal to 100.
    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_ticketquantity(self, *_):
        # login as test user
        self.login()
        # Positive case is covered under test R4.7

        # NEGATIVE: ZERO QUANTITY
        # fill in ticket information
        self.type("#sell-quantity","0")
        self.type("#sell-name","ticket1")
        self.type("#sell-price","100")
        self.type("#sell-expiration-date","20210901")
        # click sell button
        self.click('input[id="btn-sell-submit"]')
        # make sure it gives proper error message
        self.assert_element("#sellMessage")
        self.assert_text("The quantity of the tickets has to be between 1 and 100.", "#sellMessage")
        
        # NEGATIVE: QUANTITY GREATER THAN 100
        # fill in ticket information
        self.type("#sell-quantity","101")
        self.type("#sell-name","ticket1")
        self.type("#sell-price","100")
        self.type("#sell-expiration-date","20210901")
        # click sell button
        self.click('input[id="btn-sell-submit"]')
        # make sure it gives proper error message
        self.assert_element("#sellMessage")
        self.assert_text("The quantity of the tickets has to be between 1 and 100.", "#sellMessage")
    
    # Test Case R4.4 - Price has to be of range [10, 100]
    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_ticketprice(self,*_):
        # login as test user
        self.login()
        # Positive case is covered under test R4.7

        # NEGATIVE: PRICE LESS THAN 10
        # fill in ticket information
        self.type("#sell-quantity","1")
        self.type("#sell-name","ticket1")
        self.type("#sell-price","5")
        self.type("#sell-expiration-date","20210901")
        # click sell button
        self.click('input[id="btn-sell-submit"]')
        # make sure it gives proper error message
        self.assert_element("#sellMessage")
        self.assert_text("The price has to be between $10 and $100.", "#sellMessage")
        
        # NEGATIVE: PRICE MORE THAN 100
        # fill in ticket information
        self.type("#sell-quantity","1")
        self.type("#sell-name","ticket1")
        self.type("#sell-price","101")
        self.type("#sell-expiration-date","20210901")
        # click sell button
        self.click('input[id="btn-sell-submit"]')
        # make sure it gives proper error message
        self.assert_element("#sellMessage")
        self.assert_text("The price has to be between $10 and $100.", "#sellMessage")

    # Test Case R4.5 - Date must be given in the format YYYYMMDD (e.g. 20200901)
    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_ticketdateformat(self,*_):
        # login as test user
        self.login()
        # Positive case is covered under test R4.7

        # NEGATIVE: fill in ticket information with incorrect date format
        self.type("#sell-quantity","1")
        self.type("#sell-name","ticket1")
        self.type("#sell-price","100")
        self.type("#sell-expiration-date","2021-09-01")
        # click sell button
        self.click('input[id="btn-sell-submit"]')
        # make sure it gives proper error message
        self.assert_element("#sellMessage")
        self.assert_text("The date has to be in the format 'YYYYMMDD'.", "#sellMessage")
    
    # Test Case R4.6 - For any errors, redirect back to / and show an error message
    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_ticketerror(self,*_):
        # login as test user
        self.login()
        # Create error
        self.type("#sell-quantity","1")
        self.type("#sell-name","ticket1")
        self.type("#sell-price","100")
        self.type("#sell-expiration-date","2021-09-01")
        # click sell button
        self.click('input[id="btn-sell-submit"]')
        # make sure an error message occurs
        self.assert_element("#sellMessage")
        self.assert_text("Error:", "#sellMessage")
        # ensure it redirects to home page (/)
        self.assert_element("#welcome-header")
        self.assert_text("Welcome test_frontend", "#welcome-header")

    # Test Case R4.7 - 	The added new ticket information will be posted on the user profile page
    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_ticketposted(self,*_):
        # login as test user
        self.login()
        # fill in correct ticket information
        self.type("#sell-quantity","1")
        self.type("#sell-name","ticket1")
        self.type("#sell-price","100")
        self.type("#sell-expiration-date","20210901")
        # click sell button
        self.click('input[id="btn-sell-submit"]')
        # verify on homepage
        self.assert_element("#tickets-header")
        # ensure that success message is displayed
        self.assert_element("#sellMessage")
        self.assert_text("Listing posted successful", "#sellMessage")

    # Test Case R4.8 was completed along with R4.2 above. (The name of the tickets has to contain at least 6 characters)

    # Test Case R4.9 - The new tickets must not be expired
    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_ticketexpired(self,*_):
        # login as test user
        self.login()
        # Positive case is covered under test R4.7

        # NEGATIVE: fill in expired ticket information
        self.type("#sell-quantity","1")
        self.type("#sell-name","ticket1")
        self.type("#sell-price","100")
        self.type("#sell-expiration-date","20090901")
        # click sell button
        self.click('input[id="btn-sell-submit"]')
        # make sure it gives proper error message
        self.assert_element("#sellMessage")
        self.assert_text("The date cannot be expired.", "#sellMessage")