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


# Moch a sample user
test_user = User(
    email='test_frontend@test.com',
    name='test_frontend',
    password=generate_password_hash('Testfrontend123!'),
    balance=5000

)


# Moch some sample tickets
test_tickets = [
    {'name': 't1', 'price': '100', 'email': 'test_frontend@test.com', 'date': '20200901'}
]


class FrontEndHomePageTest(BaseCase):

    # Test Case R1.1 - If the user hasn't logged in, show the login page
    def test_forced_login_page(self, *_):
        # open homepage for it to redirect to /login
        self.open(base_url + '/')
        # give it one second to redirect
        self.wait(1)
        # make sure it shows the login page
        self.assert_element('#message')
        self.assert_text('Please login', '#message')

    # Test Case R1.2 - the login page has a message that by default says 'please login'
    def test_login_page(self, *_):
        # open loginpage
        self.open(base_url + '/login')
        # make sure it shows the login page
        self.assert_element('#message')
        self.assert_text('Please login', '#message')

    # Test case R1.3 - If the user has logged in, redirect to the user profile page
    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_login_success(self, *_):

        # This is a sample front end unit test to login to home page
        # and verify if the tickets are correctly listed.

        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Testfrontend123!")
        # click enter button
        self.click('input[type="submit"]')

        # after clicking on the browser (the line above)
        # the front-end code is activated
        # and tries to call get_user function.
        # The get_user function is supposed to read data from database
        # and return the value. However, here we only want to test the
        # front-end, without running the backend logics.
        # so we patch the backend to return a specific user instance,
        # rather than running that program. (see @ annotations above)

        # open home page
        self.open(base_url)
        # test if the page loads correctly
        self.assert_element("#welcome-header")
        self.assert_text("Welcome test_frontend", "#welcome-header")
        self.assert_element("#tickets-header")

    # Test case R1.4 - The login page provides a login form which requests two fields: email and passwords
    def test_login_fields(self, *_):
        # open login page
        self.open(base_url + '/login')
        self.assert_element('#email')
        self.assert_element('#password')


    # TODO: Test case R1.5 - The login form can be submitted as a POST request to the current URL (/login)

    # TODO: Test case has been taken care of by test R1.3

    # Test case R1.6 - Email and password both cannot be empty
    def test_email_password_empty(self, *_):
        # open login page
        self.open(base_url + '/login')
        # try to login without typing anything
        self.click('input[type="submit"]')
        # verify youre still on login page
        self.assert_element('#message')
        self.assert_text('Please login', '#message')

        # TRY TO LOGIN WITH JUST EMAIL
        self.type("#email", "test_frontend@test.com")
        self.click('input[type="submit"]')
        # verify youre still on login page
        self.assert_element('#message')
        self.assert_text('Please login', '#message')

        # TRY TO LOGIN WITH JUST PASSWORD
        # open login page
        self.open(base_url + '/login')
        self.type("#password", "Testfrontend123!")
        # click enter button
        self.click('input[type="submit"]')
        # verify youre still on login page
        self.assert_element('#message')
        self.assert_text('Please login', '#message')

    # Test case R1.7 - Email has to follow addr-spec defined in RFC 5322 - negative
    # Dont need positive case because positive case is tested in R1.3
    @patch('qa327.backend.get_user', return_value=test_user)
    def test_login_email_format(self, *_):
        # NO @
        # open login page
        self.open(base_url + '/login')
        # fill wrong email and password
        self.type("#email", "test_frontendtest.com")
        self.type("#password", "Testfrontend123!")
        # click enter button
        self.click('input[type="submit"]')
        # make sure it shows proper error message
        self.assert_element("#message")
        self.assert_text("email/password format is incorrect.", "#message")

        #NO .X
        # open login page
        self.open(base_url + '/login')
        # fill wrong email and password
        self.type("#email", "test_frontendtest@")
        self.type("#password", "Testfrontend123!")
        # click enter button
        self.click('input[type="submit"]')
        # make sure it shows proper error message
        self.assert_element("#message")
        self.assert_text("email/password format is incorrect.", "#message")

        # NO No prefix
        # open login page
        self.open(base_url + '/login')
        # fill wrong email and password
        self.type("#email", "@test.com")
        self.type("#password", "Testfrontend123!")
        # click enter button
        self.click('input[type="submit"]')
        # make sure it shows proper error message
        self.assert_element("#message")
        self.assert_text("email/password format is incorrect.", "#message")

        # has two @
        # open login page
        self.open(base_url + '/login')
        # fill wrong email and password
        self.type("#email", "test_frontend@te@st.com")
        self.type("#password", "Testfrontend123!")
        # click enter button
        self.click('input[type="submit"]')
        # make sure it shows proper error message
        self.assert_element("#message")
        self.assert_text("email/password format is incorrect.", "#message")

        # NO SITE
        # open login page
        self.open(base_url + '/login')
        # fill wrong email and password
        self.type("#email", "test_frontend@.com")
        self.type("#password", "Testfrontend123!")
        # click enter button
        self.click('input[type="submit"]')
        # make sure it shows proper error message
        self.assert_element("#message")
        self.assert_text("email/password format is incorrect.", "#message")

    # Test case R1.8 - Password has to meet the required complexity:
    # minimum length 6, at least one upper case, at least one lower case, and at least one special character
    # Dont need positive case because positive case is tested in R1.3
    @patch('qa327.backend.get_user', return_value=test_user)
    def test_login_password_format(self, *_):

        # NO CAPITALS
        # open login page
        self.open(base_url + '/login')
        # fill wrong email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "wrong_password1!")
        # click enter button
        self.click('input[type="submit"]')
        # make sure it shows proper error message
        self.assert_element("#message")
        self.assert_text("email/password format is incorrect.", "#message")

        # TOO SHORT
        # open login page
        self.open(base_url + '/login')
        # fill wrong email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "12")
        # click enter button
        self.click('input[type="submit"]')
        # make sure it shows proper error message
        self.assert_element("#message")
        self.assert_text("email/password format is incorrect.", "#message")

        # TOO LONG
        # open login page
        self.open(base_url + '/login')
        # fill wrong email and password
        self.type("#email", "test_frontend@test.com")
        self.type(
            "#password", "afdsfioosdaijfidjfiodjasgiojdsgijdioagjidsgjiosdajigOIAJSIFJ1421!")
        # click enter button
        self.click('input[type="submit"]')
        # make sure it shows proper error message
        self.assert_element("#message")
        self.assert_text("email/password format is incorrect.", "#message")

        # NO SYMBOL
        # open login page
        self.open(base_url + '/login')
        # fill wrong email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Wrong_password1")
        # click enter button
        self.click('input[type="submit"]')
        # make sure it shows proper error message
        self.assert_element("#message")
        self.assert_text("email/password format is incorrect.", "#message")

        # NO NUMBERS
        # open login page
        self.open(base_url + '/login')
        # fill wrong email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Wrong_password")
        # click enter button
        self.click('input[type="submit"]')
        # make sure it shows proper error message
        self.assert_element("#message")
        self.assert_text("email/password format is incorrect.", "#message")

    # Test case R1.9 - For any formatting errors, render the login page and show the message
    # 'email/password format is incorrect
    # R1.9 is verified by R1.8 and R1.7

    # Test case R1.10 - If email/password are correct, redirect to /
    # R1.10 is verified by R1.3

    # Test case R1.11 - Otherwise, redict to /login and show message 'email/password combination incorrect'
    def test_email_password_combo_bad(self, *_):
        self.open(base_url + '/login')
        # fill wrong email and password
        self.type("#email", "random_email@test.com")
        self.type("#password", "Wrongpassword1!")
        # click enter button
        self.click('input[type="submit"]')

        # make sure it shows proper error message
        self.assert_element("#message")
        self.assert_text("email/password combination incorrect", "#message")
