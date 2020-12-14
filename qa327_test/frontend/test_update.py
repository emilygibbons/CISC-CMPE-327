import pytest
from seleniumbase import BaseCase

from qa327_test.conftest import base_url
from unittest.mock import patch
from qa327.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

"""
This file defines all unit tests for the frontend update section.

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
    {'name': 'ticket1test', 'price': 100, 'email': 'test_frontend@test.com', 'date': '20200901'}
]


class FrontEndUpdateTesting(BaseCase):
    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def login(self, *_):
        self.open(base_url + '/login')
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Testfrontend123!")
        self.click('input[type="submit"]')

        # open home page
        self.open(base_url)

    # Test Case R5.1 - The name of the ticket has to be alphanumeric-only, and space allowed only if it is not the first or the last character.
    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_ticketname(self,*_):
        # login as test user
        self.login()
        
        # NEGATIVE: IF IT HAS A SYMBOL
        # fill in old existing ticket information
        self.type("#quantity-old","1")
        self.type("#name-old","ticket1test")
        self.type("#price-old","100")
        self.type("#expiration-date-old","20200901")
        # update ticket with symbol in name
        self.type("#quantity-new","1")
        self.type("#name-new","ticket1!")
        self.type("#price-new","100")
        self.type("#expiration-date-new","20210901")
        # click update button
        self.click('input[id="btn-update-submit"]')
        # make sure it gives proper error message
        self.assert_element("#updateMessage")
        self.assert_text("The updated name has to alphanumeric, have no spaces in the begining or end and be between 6 and 60 characters.", "#updateMessage")
        
        # NEGATIVE: IF IT STARTS WITH A SPACE
        # fill in old existing ticket information
        self.type("#quantity-old","1")
        self.type("#name-old","ticket1test")
        self.type("#price-old","100")
        self.type("#expiration-date-old","20200901")
        # update ticket starting with a space in name
        self.type("#quantity-new","1")
        self.type("#name-new"," ticket1")
        self.type("#price-new","100")
        self.type("#expiration-date-new","20210901")
        # click update button
        self.click('input[id="btn-update-submit"]')
        # make sure it gives proper error message
        self.assert_element("#updateMessage")
        self.assert_text("The updated name has to alphanumeric, have no spaces in the begining or end and be between 6 and 60 characters.", "#updateMessage")

        # NEGATIVE: IF IT ENDS WITH A SPACE
        # fill in old existing ticket information
        self.type("#quantity-old","1")
        self.type("#name-old","ticket1test")
        self.type("#price-old","100")
        self.type("#expiration-date-old","20200901")
        # update ticket ending with a space in name
        self.type("#quantity-new","1")
        self.type("#name-new","ticket1 ")
        self.type("#price-new","100")
        self.type("#expiration-date-new","20210901")
        # click update button
        self.click('input[id="btn-update-submit"]')
        # make sure it gives proper error message
        self.assert_element("#updateMessage")
        self.assert_text("The updated name has to alphanumeric, have no spaces in the begining or end and be between 6 and 60 characters.", "#updateMessage")
        
    # Test Case R5.2 - The name of the ticket is no longer than 60 characters and greater than 6 characters.
    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_ticketnamelength(self, *_):
        # login as test user
        self.login()
        # Positive case is already covered under the positive case of R5.1

        # NEGATIVE: MORE THAN 60 CHARACTERS
        # fill in old existing ticket information
        self.type("#quantity-old","1")
        self.type("#name-old","ticket1test")
        self.type("#price-old","100")
        self.type("#expiration-date-old","20200901")
        # update ticket ending with more than 60 characters
        self.type("#quantity-new","1")
        self.type("#name-new","qqqwwweeerrrtttyyyuuuiiiooopppaaasssdddfffggghhhjjjkkkllzzzxxxx")
        self.type("#price-new","100")
        self.type("#expiration-date-new","20210901")
        # click update button
        self.click('input[id="btn-update-submit"]')
        # make sure it gives proper error message
        self.assert_element("#updateMessage")
        self.assert_text("The updated name has to alphanumeric, have no spaces in the begining or end and be between 6 and 60 characters.", "#updateMessage")

        # NEGATIVE: LESS THAN 6 CHARACTERS
        # fill in old existing ticket information
        self.type("#quantity-old","1")
        self.type("#name-old","ticket1test")
        self.type("#price-old","100")
        self.type("#expiration-date-old","20200901")
        # update ticket with less than 6 characters
        self.type("#quantity-new","1")
        self.type("#name-new","t2")
        self.type("#price-new","100")
        self.type("#expiration-date-new","20210901")
        # click update button
        self.click('input[id="btn-update-submit"]')
        # make sure it gives proper error message
        self.assert_element("#updateMessage")
        self.assert_text("The updated name has to alphanumeric, have no spaces in the begining or end and be between 6 and 60 characters.", "#updateMessage")
        
    # Test Case R5.3 - The quantity of the tickets has to be more than 0, and less than or equal to 100.
    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    # QUANTITY OF ZERO
    def test_ticketquantity(self, *_):
        # login as test user
        self.login()
        # Positive case is already covered under the positive case of R5.1

        # NEGATIVE: ZERO QUANTITY
        # fill in old existing ticket information
        self.type("#quantity-old","1")
        self.type("#name-old","ticket1test")
        self.type("#price-old","100")
        self.type("#expiration-date-old","20200901")
        # update ticket with zero quantity
        self.type("#quantity-new","0")
        self.type("#name-new","ticket1")
        self.type("#price-new","100")
        self.type("#expiration-date-new","20210901")
        # click update button
        self.click('input[id="btn-update-submit"]')
        # make sure it gives proper error message
        self.assert_element("#updateMessage")
        self.assert_text("The updated quantity of tickets needs to be between 1 and 100.", "#updateMessage")
        
        # NEGATIVE: QUANTITY GREATER THAN 100
        # fill in old existing ticket information
        self.type("#quantity-old","1")
        self.type("#name-old","ticket1test")
        self.type("#price-old","100")
        self.type("#expiration-date-old","20200901")
        # update ticket with quantity greater than 100
        self.type("#quantity-new","101")
        self.type("#name-new","ticket1")
        self.type("#price-new","100")
        self.type("#expiration-date-new","20210901")
        # click update button
        self.click('input[id="btn-update-submit"]')
        # make sure it gives proper error message
        self.assert_element("#updateMessage")
        self.assert_text("The updated quantity of tickets needs to be between 1 and 100.", "#updateMessage")

    # Test Case R5.4 - Price has to be of range [10, 100]
    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_ticketprice(self, *_):
        # login as test user
        self.login()
        # Positive case is already covered under the positive case of R5.1

        # NEGATIVE: PRICE LESS THAN 10
        # fill in old existing ticket information
        self.type("#quantity-old","1")
        self.type("#name-old","ticket1test")
        self.type("#price-old","100")
        self.type("#expiration-date-old","20200901")
        # update ticket with price of 0
        self.type("#quantity-new","1")
        self.type("#name-new","ticket1")
        self.type("#price-new","0")
        self.type("#expiration-date-new","20210901")
        # click update button
        self.click('input[id="btn-update-submit"]')
        # make sure it gives proper error message
        self.assert_element("#updateMessage")
        self.assert_text("The updated price needs to be between $10 and $100.", "#updateMessage")
        
        # NEGATIVE: PRICE MORE THAN 100
        # fill in old existing ticket information
        self.type("#quantity-old","1")
        self.type("#name-old","ticket1test")
        self.type("#price-old","100")
        self.type("#expiration-date-old","20200901")
        # update ticket with price greater than 100
        self.type("#quantity-new","1")
        self.type("#name-new","ticket1")
        self.type("#price-new","101")
        self.type("#expiration-date-new","20210901")
        # click update button
        self.click('input[id="btn-update-submit"]')
        # make sure it gives proper error message
        self.assert_element("#updateMessage")
        self.assert_text("The updated price needs to be between $10 and $100.", "#updateMessage")
    # Test Case R5.5 - Date must be given in the format YYYYMMDD (e.g. 20200901)
    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_ticketdateformat(self, *_):
        # login as test user
        self.login()   
        # Positive case is already covered under the positive case of R5.1

        #NEGATIVE:
        # fill in old existing ticket information
        self.type("#quantity-old","1")
        self.type("#name-old","ticket1test")
        self.type("#price-old","100")
        self.type("#expiration-date-old","20200901")
        # update ticket with incorrect date format
        self.type("#quantity-new","1")
        self.type("#name-new","ticket1")
        self.type("#price-new","100")
        self.type("#expiration-date-new","2021-09-01")
        # click update button
        self.click('input[id="btn-update-submit"]')
        # make sure it gives proper error message
        self.assert_element("#updateMessage")
        self.assert_text("The updated exipiration date needs to be follow the 'YYYYMMDD' format.", "#updateMessage")
    
    # Test Case R5.6 - Ticket of given name must exist
    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_ticketnameexists(self, *_):
        # login as test user
        self.login()   
        # Positive case is already covered under the positive case of R5.1

        #NEGATIVE:
        # fill in old existing ticket information with non-existent name
        self.type("#quantity-old","1")
        self.type("#name-old","namedoesnotexist")
        self.type("#price-old","100")
        self.type("#expiration-date-old","20210901")
        # update ticket quantity
        self.type("#quantity-new","10")
        self.type("#name-new","namedoesnotexist")
        self.type("#price-new","100")
        self.type("#expiration-date-new","20210901")
        # click update button
        self.click('input[id="btn-update-submit"]')
        # make sure it gives proper error message
        self.assert_element("#updateMessage")
        self.assert_text("The entered ticket either does not exist or was entered incorrectly, please try again.", "#updateMessage")
    # Test Case R5.7 POSITIVE- For any errors, redirect back to / and show an error message
    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_ticketerror(self, *_):
        # login as test user
        self.login()  
        # fill in old existing ticket information with non-existent name, so that an error is created
        self.type("#quantity-old","1")
        self.type("#name-old","namedoesnotexist")
        self.type("#price-old","100")
        self.type("#expiration-date-old","20200901")
        # update ticket with incorrect date format, to create more errors
        self.type("#quantity-new","1")
        self.type("#name-new","ticket1")
        self.type("#price-new","100")
        self.type("#expiration-date-new","2021-09-01")
        # click update button
        self.click('input[id="btn-update-submit"]')
        # make sure an error message occurs
        self.assert_element("#updateMessage")
        self.assert_text("Error:", "#updateMessage")
        # ensure it redirects to home page (/)
        self.assert_element("#welcome-header")
        self.assert_text("Welcome test_frontend", "#welcome-header")

    # Test Case R5.7 NEGATIVE- For any errors, redirect back to / and show an error message
    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    #@patch('qa327.backend.ticketExists', return_value= True)
    #@patch('qa327.backend.verify_ticket', return_value= True)
    #@patch('qa327.backend.sell_ticket', return_value= True)
    #@patch('qa327.backend.delete_ticket', return_value= True)
    def test_ticketsuccess(self, *_):
        # login as test user
        self.login()  
        # NEGATIVE CASE: no errors so post update successfully
        # fill in old existing ticket information
        self.type("#quantity-old","1")
        self.type("#name-old","ticket1test")
        self.type("#price-old","100")
        self.type("#expiration-date-old","20200901")
        # update ticket 
        self.type("#quantity-new","1")
        self.type("#name-new","newticket")
        self.type("#price-new","100")
        self.type("#expiration-date-new","20210901")
        # click update button
        self.click('input[id="btn-update-submit"]')
        # make sure it gives proper success message
        self.assert_element("#updateMessage")
        self.assert_text("Listing update successful", "#updateMessage")
  