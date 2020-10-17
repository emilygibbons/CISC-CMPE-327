# Test Case R1 /login
Test data:
```
test_user = User(
    email='test_frontend@test.com',
    name='test_frontend',
    password=generate_password_hash('test_frontend')
)
```

```
test_user_false1 = User(
    email='test_frontend@test.com',
    name='test_frontend',
    password=generate_password_hash('incorrect_password')
)
```
## [GET]
#### Test Case R1.1 - If the user hasn't logged in, show the login page
Actions:

-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-  validate that current page contains  `#login-message`  element

#### Test Case R1.2 - the login page has a message that by default says 'please login'
Actions:

-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   validate that current page contains  `#login-message`  element

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
-   validate that current page contains  `#welcome-header`  element

#### Test case R1.4 - The login page provides a login form which requests two fields: email and passwords
Actions:

-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   validate that current page contains  `#email`  element
-   validate that current page contains  `#password`  element

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
-   validate that  `#submit`  button points to `#http://127.0.0.1:8081/`

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

#### Test case R1.7 - Email has to follow addr-spec defined in RFC 5322
Mocking:

-   Mock backend.get_user to return a test_user instance

Actions:
-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   enter test_user's email into element  `#email`
- validate that the `#email` element meets regex `"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"`

#### Test case R1.8 - Password has to meet the required complexity: minimum length 6, at least one upper case, at least one lower case, and at least one special character
Mocking:
-   Mock backend.get_user to return a test_user instance

Actions:
-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   enter test_user's email into element  `#password`
- validate that the `#password` element has >= 6  characters
-  validate that the `#password` element has >= 1 uppercase
- validate that the `#password` element has >= 1 lower case
- validate that the `#password` element has >= 1 special character

#### Test case R1.9 - For any formatting errors, render the login page and show the message 'email/password format is incorrect.' - Positive
Actions:
-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   validate that element `#email` form exists
-   validate that element `#password` form exists

#### Test case R1.9 - For any formatting errors, render the login page and show the message 'email/password format is incorrect.' - Negative
Actions:
-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   validate that element `#email` form does not exists
-   validate that element `#password` form does not exists
- validate that error message `email/password format is incorrect.`

#### Test case R1.10 - If email/password are correct, redirect to / NEEDS TO BE FINSIHED
Mocking:
-   Mock backend.get_user to return a test_user instance

Actions:
-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   enter test_user's email into element  `#email`
-   enter test_user's password into element  `#password`
-   click element  `input[type="submit"]`
-   open /
- validate that `login_post():` of `front_end.py` returns `code=303`

#### Test case R1.10 - Otherwise, redict to /login and show message 'email/password combination incorrect'
Mocking:
-   Mock backend.get_user to return a test_user_false1 instance

Actions:
-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   enter test_user's email into element  `#email`
-   enter test_user's password into element  `#password` 
-   click element  `input[type="submit"]`
-   open /login again
-   validate that current page contains  `email/password combination icorrect`  message


