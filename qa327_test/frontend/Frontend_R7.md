# Test Case R7
Test data:
```
test_user = User(
    email='test_frontend@test.com',
    name='test_frontend',
    password=generate_password_hash('test_frontend')
)
```
```
test_ticket = Ticket(
    owner='test_frontend@test.com',
    name='test_ticket_yo',
    quantity=10,
    price=10,
    date='20200901'
)
```
### Test Case R7.1 -  Logout will invalid the current session and redirect to the login page. After logout, the user shouldn't be able to access restricted pages.
Mocking:

-   Mock backend.get_user to return a test_user instance
-   Mock backend.get_ticket to return a test_ticket instance

Actions:

-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   enter test_user's email into element  `#email`
-   enter test_user's password into element  `#password`
-   click element  `input[type="submit"]`
- click element string `"logout"`with `<a href>` tag that redirects to login screen
- validate the current page has the `#login-message` element
-  open / 
- validate the user was denied access by and sent back to the login page by checking if the current page has the `#login-message` element
- open /sell
- validate the user was denied access by and sent back to the login page by checking if the current page has the `#login-message` element
- open /buy
- validate the user was denied access by and sent back to the login page by checking if the current page has the `#login-message` element
- open /update
- validate the user was denied access by and sent back to the login page by checking if the current page has the `#login-message` element
