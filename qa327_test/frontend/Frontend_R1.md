# Test Case R1 /login
Test data:
```
test_user = User(
    email='test_frontend@test.com',
    name='test_frontend',
    password=generate_password_hash('test_frontend')
)
```

## [GET]
#### Test Case R1.1 - If the user hasn't logged in, show the login page
Actions:

-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   open /logout (clean up)
- 
#### Test Case R1.2 - the login page has a message that by default says 'please login'
Actions:

-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   validate that current page contains  `#login-message`  element
-   open /logout (clean up)

#### Test case R1.3 - If the user has logged in, redirect to the user profile page
Mocking:

-   Mock backend.get_user to return a test_user instance

Actions:

-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   enter test_user's email into element  `#email`
-   enter test_user's password into element  `#password`
-   click element  `input[type="submit"]`
-   open /login again
-   validate that current page contains  `#login-message`  element
-   open /logout (clean up)

#### Test case R1.4 - The login page provides a login form which requests two fields: email and passwords
Actions:

-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   validate that current page contains  `#email`  element
-   validate that current page contains  `#password`  element
-   open /logout (clean up)

## [POST]

#### Test case R1.5 - The login form can be submitted as a POST request to the current URL (/login)
Mocking:

-   Mock backend.get_user to return a test_user instance

Actions:

-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   validate that current page contains  `#email`  element
-   validate that current page contains  `#password`  element
-   enter test_user's email into element  `#email`
-   enter test_user's password into element  `#password`
-   validate that current page contains  `#submit`  button
-   validate that  `#submit`  button points to `/`
-   open /logout (clean up)

#### Test case R1.6 - Email and password both cannot be empty
Mocking:

-   Mock backend.get_user to return a test_user instance

Actions:
-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   click element  `input[type="submit"]`
-   validate that current page contains  `#Please-fill-out-this-field`
-   enter test_user's email into element  `#email`
-   click element  `input[type="submit"]`
-   validate that current page contains  `#Please-fill-out-this-field`  element
- clear element `#email`
-   enter test_user's password into element  `#password`
-   click element  `input[type="submit"]`
-   validate that current page contains  `#Please-fill-out-this-field`
-   open /logout (clean up)

#### Test case R1.7 - Email has to follow addr-spec defined in RFC 5322 - Positive
Mocking:

-   Mock backend.get_user to return a test_user instance

Actions:
-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   enter test_user's email into element  `#email`
-   enter test_users password into element `#password`
-   click element  `input[type="submit"]`
-   open /
-   validate that current page contains  `#welcome-header`  element
-   open /logout (clean up)

#### Test case R1.7 - Email has to follow addr-spec defined in RFC 5322 - Negative
Mocking:

-   Mock backend.get_user to return a test_user instance

Actions:
-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   enter test_user's fake email into element  `#email`
-   enter test_users password into element `#password`
-   click element  `input[type="submit"]`
- validate that  `#error_message` shows `Email form incorrect`
-   open /logout (clean up)


#### Test case R1.8 - Password has to meet the required complexity: minimum length 6, at least one upper case, at least one lower case, and at least one special character - Positive
Mocking:
-   Mock backend.get_user to return a test_user instance

Actions:
-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
- enter test_user's email int `#email`
-   enter test_user's email password element  `#password`
-   click element  `input[type="submit"]`
-   open /
-   validate that current page contains  `#welcome-header`  element
-   open /logout (clean up)

#### Test case R1.8 - Password has to meet the required complexity: minimum length 6, at least one upper case, at least one lower case, and at least one special character - Negative
Mocking:
-   Mock backend.get_user to return a test_user instance

Actions:
-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
- enter test_user's email into `#email`
-   enter `abc`  into element  `#password`
- validate that the `#error_message` shows `Password not long enough`
- enter test_user's email into `#email`
- enter `abcd123!` into element  `#password`
- validate that the `#error_message` shows `Password needs a capital letter`
- enter test_user's email into `#email`
- enter `ABCD123!` into element  `#password`
- validate that the `#error_message` shows `Password needs a lowercase letter`
- enter test_user's email into `#email`
- enter `Abcd123` into element  `#password`
- validate that the `#error_message` shows `Password needs a special character`
-   open /logout (clean up)

#### Test case R1.9 - For any formatting errors, render the login page and show the message 'email/password format is incorrect.' - Positive
Mocking:
-   Mock backend.get_user to return a test_user instance

Actions:
-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   enter test_user's email into element  `#email`
-   enter test_user's password into element  `#password`
-   click element  `input[type="submit"]`
-   open /login again
-   validate that current page contains  `#login-message`  element
-   open /logout (clean up)

#### Test case R1.9 - For any formatting errors, render the login page and show the message 'email/password format is incorrect.' - Negative
Mocking:
-   Mock backend.get_user to return a test_user instance

Actions:
-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   enter `this_aint_no_email@@@emailRnotUS.com` into element  `#email`
-   enter test_user's password into element  `#password`
-   click element  `input[type="submit"]`
- validate that error message `email/password format is incorrect.`
-   open /logout (clean up)

#### Test case R1.10 - If email/password are correct, redirect to / 
Mocking:
-   Mock backend.get_user to return a test_user instance

Actions:
-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   enter test_user's email into element  `#email`
-   enter test_user's password into element  `#password`
-   click element  `input[type="submit"]`
-   open /
-   validate that current page contains  `#welcome-header`  element
-   open /logout (clean up)

#### Test case R1.11 - Otherwise, redict to /login and show message 'email/password combination incorrect'
Mocking:
-   Mock backend.get_user to return a test_user_false1 instance

Actions:
-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   enter test_user's email into element  `#email`
-   enter test_user's fake password into element  `#password` 
-   click element  `input[type="submit"]`
-   open /login again
-   validate that current page contains  `email/password combination icorrect`  message
-   open /logout (clean up)


