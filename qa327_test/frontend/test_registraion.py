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


class FrontEndHomePageTest(BaseCase):
    # Test Case R2.1 - If the user has logged in, redirect back to the user profile page
    @patch('qa327.backend.get_user', return_value=test_user)
    def test_login_success(self, *_):
        # open login page

        self.open(base_url + '/login')
        # fill email and password

        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Testfrontend123!")
        # click enter button

        self.click('input[type="submit"]')
        # open home page

        self.open(base_url)
        # test if the page loads correctly

        self.assert_element("#welcome-header")
        self.assert_text("Welcome test_frontend", "#welcome-header")

    # Test Case R2.2 - otherwise, show the user registration page

    def test_show_register(self, *_):
        # open login
        self.open(base_url + '/login')
        # go to register page
        self.click_link_text('Register')
        # verify that you are on register page
        self.assert_element("#message")
        self.assert_text("Please enter info below", '#message')

    # the registration page shows a registration form requesting: email, user name, password, password2
    def test_registration_page_format(self, *_):
        # open register
        self.open(base_url + '/register')
        # verify that these fields exist
        self.assert_element('#email')
        self.assert_element('#password')
        self.assert_element('#name')
        self.assert_element('#password2')

    # TODO Test Case R2.4 - Test case has been taken care of by test R2.1

    # Test Case R2.5 - Email, password, password2 all have to satisfy the same requirements as defined in R1
    # Testing all different cases with different boxes empy, corresponding box can be seen in function names

    def test_register_everything_not_empty(self, *_):
        # IF NOTHING IS ENTERED
        # open register
        self.open(base_url + '/register')
        # click enter button
        self.click('input[type="submit"]')
        # verify that it did not allow user to submit
        self.assert_element("#message")
        self.assert_text("Please enter info below", '#message')

    def test_register_email_not_empty(self, *_):
        # IF ONLY EMAIL IS ENTERED
        # open register
        self.open(base_url + '/register')
        self.type("#email", "test_frontend@test.com")
        # click enter button
        self.click('input[type="submit"]')
        # verify that it did not allow user to submit
        self.assert_element("#message")
        self.assert_text("Please enter info below", '#message')

    def test_register_name_not_empty(self, *_):
        # IF ONLY NAME IS ENTERED
        # open register
        self.open(base_url + '/register')
        self.type("#name", "bob")
        # click enter button
        self.click('input[type="submit"]')
        # verify that it did not allow user to submit
        self.assert_element("#message")
        self.assert_text("Please enter info below", '#message')

    def test_register_password1_not_empty(self, *_):
        # IF ONLY PASSWORD IS ENTERED
        # open register
        self.open(base_url + '/register')
        self.type("#password", "TestPassword123!")
        # click enter button
        self.click('input[type="submit"]')
        # verify that it did not allow user to submit
        self.assert_element("#message")
        self.assert_text("Please enter info below", '#message')

    def test_register_password2_not_empty(self, *_):
        # IF ONLY PASSWORD2 IS ENTERED
        # open register
        self.open(base_url + '/register')
        self.type("#password2", "TestPassword123!")
        # click enter button
        self.click('input[type="submit"]')
        # verify that it did not allow user to submit
        self.assert_element("#message")
        self.assert_text("Please enter info below", '#message')

    # test all incorrect email formats and see if program catches it
    def test_email_format(self, *_):
        # open register
        self.open(base_url + '/register')

        # NO @
        # open register
        self.open(base_url + '/register')
        # fill wrong email and password
        self.type("#email", "test_frontendtest.com")
        self.type('#name', 'Bill')
        self.type("#password", "Testfrontend123!")
        self.type("#password2", "Testfrontend123!")
        # click enter button
        self.click('input[type="submit"]')
        # make sure it shows proper error message
        self.assert_element("#message")
        self.assert_text("email format is incorrect.", "#message")

        #NO .X
        # open register
        self.open(base_url + '/register')
        # fill wrong email and password
        self.type("#email", "test_frontendtest@")
        self.type('#name', 'Bill')
        self.type("#password", "Testfrontend123!")
        self.type("#password2", "Testfrontend123!")
        # click enter button
        self.click('input[type="submit"]')
        # make sure it shows proper error message
        self.assert_element("#message")
        self.assert_text("email format is incorrect.", "#message")

        # NO No prefix
        # open register
        self.open(base_url + '/register')
        self.type("#email", "@test.com")
        self.type('#name', 'Bill')
        self.type("#password", "Testfrontend123!")
        self.type("#password2", "Testfrontend123!")
        # click enter button
        self.click('input[type="submit"]')
        # make sure it shows proper error message
        self.assert_element("#message")
        self.assert_text("email format is incorrect.", "#message")

        # has two @
        # open register
        self.open(base_url + '/register')
        # fill wrong email and password
        self.type("#email", "test_frontend@te@st.com")
        self.type('#name', 'Bill')
        self.type("#password", "Testfrontend123!")
        self.type("#password2", "Testfrontend123!")
        # click enter button
        self.click('input[type="submit"]')
        # make sure it shows proper error message
        self.assert_element("#message")
        self.assert_text("email format is incorrect.", "#message")

        # NO SITE
        # open register
        self.open(base_url + '/register')
        # fill wrong email and password
        self.type("#email", "test_frontend@.com")
        self.type('#name', 'Bill')
        self.type("#password", "Testfrontend123!")
        self.type("#password2", "Testfrontend123!")
        # click enter button
        self.click('input[type="submit"]')
        # make sure it shows proper error message
        self.assert_element("#message")
        self.assert_text("email format is incorrect.", "#message")

    # test all possible incorrect password formats and see if the program catches it
    def test_password_format(self, *_):
        # NO CAPITALS
        # open register
        self.open(base_url + '/register')
        # fill wrong email and password
        self.type("#email", "test_frontend@test.com")
        self.type('#name', 'Bill')
        self.type("#password", "wrong_password1!")
        self.type("#password2", "wrong_password1!")
        # click enter button
        self.click('input[type="submit"]')
        # make sure it shows proper error message
        self.assert_element("#message")
        self.assert_text("password format incorrect.", "#message")

        # TOO SHORT
        # open register
        self.open(base_url + '/register')
        # fill wrong email and password

        self.type("#email", "test_frontend@test.com")
        self.type('#name', 'Bill')
        self.type("#password", "12")
        self.type("#password2", "12")
        # click enter button

        self.click('input[type="submit"]')
        # make sure it shows proper error message

        self.assert_element("#message")

        self.assert_text("password format incorrect.", "#message")

        # TOO LONG
        # open register
        self.open(base_url + '/register')
        # fill wrong email and password
        self.type("#email", "test_frontend@test.com")
        self.type('#name', 'Bill')
        self.type(
            "#password", "afdsfioosdaijfidjfiodjasgiojdsgijdioagjidsgjiosdajigOIAJSIFJ1421!")
        self.type(
            "#password2", "afdsfioosdaijfidjfiodjasgiojdsgijdioagjidsgjiosdajigOIAJSIFJ1421!")
        # click enter button
        self.click('input[type="submit"]')
        # make sure it shows proper error message
        self.assert_element("#message")
        self.assert_text("password format incorrect.", "#message")

        # NO SYMBOL
        # open register
        self.open(base_url + '/register')
        # fill wrong email and password
        self.type("#email", "test_frontend@test.com")
        self.type('#name', 'Bill')
        self.type("#password", "Wrongpassword1")
        self.type("#password2", "Wrongpassword1")
        # click enter button
        self.click('input[type="submit"]')
        # make sure it shows proper error message
        self.assert_element("#message")
        self.assert_text("password format incorrect.", "#message")

        # NO NUMBERS
        # open register
        self.open(base_url + '/register')
        # fill wrong email and password
        self.type("#email", "test_frontend@test.com")
        self.type('#name', 'Bill')
        self.type("#password", "Wrong!password")
        self.type("#password2", "Wrong!password")
        # click enter button
        self.click('input[type="submit"]')
        # make sure it shows proper error message
        self.assert_element("#message")
        self.assert_text("password format incorrect.", "#message")

    # Test Case R2.6 - Password and password2 have to be exactly the same
    def test_passwords_are_same(self, *_):
        # open register
        self.open(base_url + '/register')
        # fill wrong email and password
        self.type("#email", "test_frontend@test.com")
        self.type('#name', 'Bill')
        self.type("#password", "Helloworld123!")
        self.type("#password2", "Goodbyeworld321!")
        # click enter button
        self.click('input[type="submit"]')
        # make sure it gives proper error message
        self.assert_element("#message")
        self.assert_text("passwords not equal", "#message")

    # Test Case R2.7 - User name has to be non-empty, alphanumeric-only,
    # and space allowed only if it is not the first or the last character.
    # NOTE: possibilty of being empty was tested in R2.5, will not be testing this again
    def test_user_name_format(self, *_):

        # IF IT HAS A SYMBOL
        # open register
        self.open(base_url + '/register')
        # fill wrong email and password
        self.type("#email", "test_frontend@test.com")
        self.type('#name', 'Bill!@#')
        self.type("#password", "Helloworld123!")
        self.type("#password2", "Helloworld123!")
        # click enter button
        self.click('input[type="submit"]')
        # make sure it gives proper error message
        self.assert_element("#message")
        self.assert_text("username format incorrect.", "#message")

        # IF IT STARTS WITH A SPACE
        # open register
        self.open(base_url + '/register')
        # fill wrong email and password
        self.type("#email", "test_frontend@test.com")
        self.type('#name', ' Bill')
        self.type("#password", "Helloworld123!")
        self.type("#password2", "Helloworld123!")
        # click enter button
        self.click('input[type="submit"]')
        # make sure it gives proper error message
        self.assert_element("#message")
        self.assert_text("username format incorrect.", "#message")

        # IF IT ENDS WITH A SPACE
        # open register
        self.open(base_url + '/register')
        # fill wrong email and password
        self.type("#email", "test_frontend@test.com")
        self.type('#name', 'Bill ')
        self.type("#password", "Helloworld123!")
        self.type("#password2", "Helloworld123!")
        # click enter button
        self.click('input[type="submit"]')
        # make sure it gives proper error message
        self.assert_element("#message")
        self.assert_text("username format incorrect.", "#message")

    def test_user_name_length(self, *_):
        # IF IT IS 2 CHARACTERS OR LESS
        # open register
        self.open(base_url + '/register')
        # fill wrong email and password
        self.type("#email", "test_frontend@test.com")
        self.type('#name', 'a')
        self.type("#password", "Helloworld123!")
        self.type("#password2", "Helloworld123!")
        # click enter button
        self.click('input[type="submit"]')
        # make sure it gives proper error message
        self.assert_element("#message")
        self.assert_text("username format incorrect.", "#message")

        # IF IT IS MORE THAN 20 CHARACTERS
        # open register
        self.open(base_url + '/register')
        # fill wrong email and password
        self.type("#email", "test_frontend@test.com")
        self.type(
            '#name', 'dsfajgijaosijgiodjfijdjfoisajfiosajfiojdsiofjdiosafjiosajsfiojdiofjisodajfdiosahfdahdghioa')
        self.type("#password", "Helloworld123!")
        self.type("#password2", "Helloworld123!")
        # click enter button
        self.click('input[type="submit"]')
        # make sure it gives proper error message
        self.assert_element("#message")
        self.assert_text("username format incorrect.", "#message")

    # NOTE: Test Case R2.10 - For any formatting errors, redirect back to /login
    #  and show message '{} format is incorrect.'.format(the_corresponding_attribute)
    #
    # This case has already been taken care of

    # Test Case R2.11 - If the email already exists, show message 'this email has been ALREADY used'
    @patch('qa327.backend.register_user', return_value=test_user)
    @patch('qa327.backend.get_user', return_value=test_user)
    def test_user_already_exists(self, *_):
        # open register
        self.open(base_url + '/register')
        # fill same email and password
        self.type("#email", "test_frontend@test.com")
        self.type('#name', 'testfrontend')
        self.type("#password", "Testfrontend123!")
        self.type("#password2", "Testfrontend123!")
        # click enter button
        self.click('input[type="submit"]')
        self.assert_element("#message")
        # click enter button
        self.click('input[type="submit"]')
        self.assert_text("this email has been ALREADY used", "#message")

    # Test Case R2.12 - If no error regarding the inputs following the rules above, create a new user,
    # set the balance to 5000, and go back to the /login page
    @patch('qa327.backend.register_user', return_value=True)
    @patch('qa327.backend.get_user', return_value=False)
    def test_clean_register(self, *_):
        # open register
        self.open(base_url + '/register')
        # fill same email and password
        self.type("#email", "test_frontend@test.com")
        self.type('#name', "testuser")
        self.type("#password", "Testfrontend123!")
        self.type("#password2", "Testfrontend123!")
        # click enter button
        self.click('input[type="submit"]')
        # make sure it shows the login page
        self.assert_element('#message')
        self.assert_text('Please login', '#message')
