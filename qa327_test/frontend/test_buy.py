import pytest
from seleniumbase import BaseCase

from qa327_test.conftest import base_url
from unittest.mock import patch
from qa327.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

"""
This file defines all unit tests for the frontend buy section.

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

# Mock another sample user

test_user2 = User(
    email='test_frontend2@test.com',
    name='test_frontend2',
    password=generate_password_hash('Testfrontend123!'),
    balance=1 

)

# Mock some sample tickets

test_tickets = [
    {'name': 'ticket1', 'price': 100, 'email': 'test_frontend@test.com', 'date': '20210901'}
]


class FrontEndBuyTesting(BaseCase):
    #login user 1
    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def login(self, *_):
        self.open(base_url + '/login')
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Testfrontend123!")
        self.click('input[type="submit"]')

        # open home page
        self.open(base_url)
    
    #login user 2
    @patch('qa327.backend.get_user', return_value=test_user2)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def login2(self, *_):
        self.open(base_url + '/login')
        self.type("#email", "test_frontend2@test.com")
        self.type("#password", "Testfrontend123!")
        self.click('input[type="submit"]')

        # open home page
        self.open(base_url)

    # Test Case R6.1 - The name of the ticket has to be alphanumeric-only, and space allowed only if it is not the first or the last character.
    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    @patch('qa327.backend.ticketExists', return_value= True)
    def test_ticketname(self,*_):
        # login as test user
        self.login()
        # Positive case covered in R6.6

        # NEGATIVE: IF IT HAS A SYMBOL
        # fill in ticket information 
        self.type("#buy-name","ticket1!")
        self.type("#buy-quantity","1")
        # click buy button
        self.click('input[id="btn-buy-submit"]')
        # make sure it gives proper error message
        self.assert_element("#buyMessage")
        self.assert_text("The name has to alphanumeric, have no spaces in the beginning or end and be between 6 and 60 characters.", "#buyMessage")

        # NEGATIVE: IF IT STARTS WITH A SPACE
        # fill in ticket information
        self.type("#buy-name"," ticket1")
        self.type("#buy-quantity","1")
        # click buy button
        self.click('input[id="btn-buy-submit"]')
        # make sure it gives proper error message
        self.assert_element("#buyMessage")
        self.assert_text("The name has to alphanumeric, have no spaces in the beginning or end and be between 6 and 60 characters.", "#buyMessage")

        # NEGATIVE: IF IT ENDS WITH A SPACE
        # fill in ticket information
        self.type("#buy-name","ticket1 ")
        self.type("#buy-quantity","1")
        # click buy button
        self.click('input[id="btn-buy-submit"]')
        # make sure it gives proper error message
        self.assert_element("#buyMessage")
        self.assert_text("The name has to alphanumeric, have no spaces in the beginning or end and be between 6 and 60 characters.", "#buyMessage")

    # Test Case R6.2 - The name of the ticket is no longer than 60 characters and more than 6 characters.
    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    @patch('qa327.backend.ticketExists', return_value= True)
    def test_ticketlength(self,*_):
        # login as test user
        self.login()
        # Positive case is already covered under the positive case of R6.6

        # NEGATIVE: MORE THAN 60 CHARACTERS
        # fill in ticket information
        self.type("#buy-name","qqqwwweeerrrtttyyyuuuiiiooopppaaasssdddfffggghhhjjjkkkllzzzxxxx")
        self.type("#buy-quantity","1")
        # click buy button
        self.click('input[id="btn-buy-submit"]')
        # make sure it gives proper error message
        self.assert_element("#buyMessage")
        self.assert_text("The name has to alphanumeric, have no spaces in the beginning or end and be between 6 and 60 characters.", "#buyMessage")

        # NEGATIVE: LESS THAN 6 CHARACTERS
        # fill in ticket information
        self.type("#buy-name","t2")
        self.type("#buy-quantity","1")
        # click buy button
        self.click('input[id="btn-buy-submit"]')
        # make sure it gives proper error message
        self.assert_element("#buyMessage")
        self.assert_text("The name has to alphanumeric, have no spaces in the beginning or end and be between 6 and 60 characters.", "#buyMessage")

    # Test Case R6.3 - The quantity of the tickets has to be more than 0, and less than or equal to 100.
    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    @patch('qa327.backend.ticketExists', return_value= True)
    def test_ticketquantity(self, *_):
        # login as test user
        self.login()
        # Positive case is already covered under the positive case of R6.6

        # NEGATIVE: ZERO QUANTITY
        # fill in ticket information
        self.type("#buy-name","ticket1")
        self.type("#buy-quantity","0")
        # click buy button
        self.click('input[id="btn-buy-submit"]')
        # make sure it gives proper error message
        self.assert_element("#buyMessage")
        self.assert_text("The quantity of the tickets has to be between 1 and 100.", "#buyMessage")
        
        # NEGATIVE: QUANTITY GREATER THAN 100
        # fill in ticket information
        self.type("#buy-name","ticket1")
        self.type("#buy-quantity","101")
        # click buy button
        self.click('input[id="btn-buy-submit"]')
        # make sure it gives proper error message
        self.assert_element("#buyMessage")
        self.assert_text("The quantity of the tickets has to be between 1 and 100.", "#buyMessage")

    # Test Case R6.4(a) - The ticket name exists in the database and the quantity is more than the quantity requested to buy
    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_ticketdoesnotexist(self, *_):
        # login as test user
        self.login()
        # Positive case is already covered under the positive case of R6.6

        #NEGATIVE : NAME DOES NOT EXIST
        # fill in ticket information
        self.type("#buy-name","ticketdoesnotexist")
        self.type("#buy-quantity","1")
        # click buy button
        self.click('input[id="btn-buy-submit"]')
        # make sure it gives proper error message
        self.assert_element("#buyMessage")
        self.assert_text("Ticket does not exist.", "#buyMessage")
    # Test Case R6.4(b) - The ticket name exists in the database and the quantity is more than the quantity requested to buy
    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    @patch('qa327.backend.ticketExists', return_value= True)
    def test_notenoughtickets(self, *_):
        # login as test user
        self.login()
        #NEGATIVE : Quantity requested is more than in stock
        # fill in ticket information
        self.type("#buy-name","ticket1")
        self.type("#buy-quantity","50")
        # click buy button
        self.click('input[id="btn-buy-submit"]')
        # make sure it gives proper error message
        self.assert_element("#buyMessage")
        self.assert_text("The specified quantity of tickets not available.", "#buyMessage")

    # Test Case R6.5 POSITIVE - The user has MORE balance than the ticket price * quantity + service fee (35%) + tax (5%)
    #Positive case is already covered under the positive case of R6.6(b)

    # Test Case R6.5 NEGATIVE - The user has LESS balance than the ticket price * quantity + service fee (35%) + tax (5%)
    @patch('qa327.backend.get_user', return_value=test_user2)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    @patch('qa327.backend.ticketExists', return_value= True)
    @patch('qa327.backend.isEnoughTickets', return_value= True)
    @patch('qa327.backend.getTicketsPrice', return_value= 100)
    
    def test_notenoughbalance(self, *_):
        # login as test user 2
        self.login2()
        # fill in ticket information
        self.type("#buy-name","ticket1")
        self.type("#buy-quantity","1")
        # click buy button
        self.click('input[id="btn-buy-submit"]')
        # make sure it gives proper error message
        self.assert_element("#buyMessage")
        self.assert_text("Your balance is too low!", "#buyMessage")

    # Test Case R6.6(a) - For any errors, redirect back to / and show an error message
    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    @patch('qa327.backend.ticketExists', return_value= True)
    def test_ticketredirect(self, *_):
        # login as test user
        self.login()
        # Create error
        self.type("#buy-name","t1")
        self.type("#buy-quantity","1")
        # click sell button
        self.click('input[id="btn-buy-submit"]')
        # make sure an error message occurs
        self.assert_element("#buyMessage")
        self.assert_text("Error:", "#buyMessage")
        # ensure it redirects to home page (/)
        self.assert_element("#welcome-header")
        self.assert_text("Welcome test_frontend", "#welcome-header")

    # Test Case R6.6(b)- For any errors, redirect back to / and show an error message
    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    @patch('qa327.backend.ticketExists', return_value= True)
    @patch('qa327.backend.isEnoughTickets', return_value= True)

    # Negative: no errors
    def test_ticketsuccess(self, *_):
        # login as test user
        self.login()

        # fill in ticket information
        self.type("#buy-name","ticket1")
        self.type("#buy-quantity","1")
        # click buy button
        self.click('input[id="btn-buy-submit"]')
        # make sure it gives proper success message
        self.assert_element("#buyMessage")
        self.assert_text("Purchase successful", "#buyMessage")


