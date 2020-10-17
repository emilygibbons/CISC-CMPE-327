# Test Case R3
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
### Test Case R3.1 - If the user is not logged in, redirect to login page
Actions:

- open /logout (to invalidate any logged-in sessions that may exist)
- open / 
- validate the current page contains the `<h4 id='message'>`

### Test Case R3.2 - This page shows a header 'Welcome {}'.format(user.name)

Mocking:

- Mock backeng.get_user to return a test_user instance.

Actions: 

-  open /logout (to invalidate any logged-in sessions that may exist)
- open /login
-  enter test_user's email into element  `#email`
-  enter test_user's password into element  `#password`
-  click element  `input[type="submit"]`
- open /
- validate the current page contains `#welcome-header` element

### Test Case R3.3 - This page shows user balance.
Mocking:
- mock backend.get_user to return a test_user instance

Actions:
- logout(to invalidate any logged-in sessions that may exist)
- open /login
-  enter test_user's email into element  `#email`
-  enter test_user's password into element  `#password`
-  click element  `input[type="submit"]`
- open /
- validate the page contains the `<div id='balance'>`

### Test Case R3.4 - This page shows a logout link, pointing to /logout
Mocking:
- mock backend.get_user to return a test_user instance
- 
Actions:
 logout(to invalidate any logged-in sessions that may exist)
- open /login
-  enter test_user's email into element  `#email`
-  enter test_user's password into element  `#password`
-  click element  `input[type="submit"]`
- open /
- click element with `<a href>`tag with the text "logout"
-  validate the current page contains the `<h4 id='message'>`

### Test Case R3.5 - This page lists all available tickets. Information including the quantity of each ticket, the owner's email, and the price, for tickets that are not expired.
- mock backend.get_user to return a test_user instance

Actions:
- logout(to invalidate any logged-in sessions that may exist)
- open /login
-  enter test_user's email into element  `#email`
-  enter test_user's password into element  `#password`
-  click element  `input[type="submit"]`
- open /
- validate the current page contains the  `<div id = 'ticket'>` div tag
- validate sub `<div>` tags for each individual ticket entry for the fields owners email, the price, and the tickets

### Test Case R3.6 - This page contains a form that a user can submit new tickets for sell. Fields: name, quantity, price, expiration date
Mocking
- mock backend.get_user to return a test_user instance

Actions:
- logout(to invalidate any logged-in sessions that may exist)
- open /login
-  enter test_user's email into element  `#email`
-  enter test_user's password into element  `#password`
-  click element  `input[type="submit"]`
- open /
- validate the current page contains the `<div id = 'sell-form'>` div tag with the fields name, quantity, price, expiration date

### Test Case R3.7 -  This page contains a form that a user can buy new tickets. Fields: name, quantity
Mocking:
- mock backend.get_user to return a test_user instance

Actions:
- logout(to invalidate any logged-in sessions that may exist)
- open /login
-  enter test_user's email into element  `#email`
-  enter test_user's password into element  `#password`
-  click element  `input[type="submit"]`
- open /
- validate the current page contains the `<div id = 'buy-form>` div tag with the fields name, quantity

### Test Case R3.8 - This page contains a form that a user can update existing tickets. Fields: name, quantity, price, expiration date.
Mocking:
- mock backend.get_user to return a test_user instance

Actions:
- logout(to invalidate any logged-in sessions that may exist)
- open /login
-  enter test_user's email into element  `#email`
-  enter test_user's password into element  `#password`
-  click element  `input[type="submit"]`
- open /
- validate the current page contains the `<div id = 'update-ticket-form'>` div tag with the fields name, quantity, price, expiration date

### Test Case R3.9 - The ticket-selling form can be posted to /sell
Mocking:
- mock backend.get_user to return a test_user instance

Actions:
- logout(to invalidate any logged-in sessions that may exist)
- open /login
-  enter test_user's email into element  `#email`
-  enter test_user's password into element  `#password`
-  click element  `input[type="submit"]`
- open /
- enter a test_tickets name into the sell form element `#name`
- enter a test_tickets quantity into the sell form element`#quantity`
- enter a test_tickets price into the sell form element `#price`
- enter a test_ticket expiration date into the sell form element `#expiration-date`
- click the element `input[type="submit"]`
- validate the current page contains the `#sell_message`element `succesful`

### Test Case R3.10 - The ticket-buying form can be posted to /buy
Mocking:
- mock backend.get_user to return a test_user instance

Actions:
- logout(to invalidate any logged-in sessions that may exist)
- open /login
-  enter test_user's email into element  `#email`
-  enter test_user's password into element  `#password`
-  click element  `input[type="submit"]`
- open /
- enter a test_tickets name into the sell form element `#name`
- enter a test_tickets quantity into the sell form element`#quantity`
- click the element `input[type="submit"]`
- validate the current page contains the `#buy-message`element `successful`

### Test Case R3.11 - The ticket-update form can be posted to /update

Mocking:
- mock backend.get_user to return a test_user instance

Actions:
- logout(to invalidate any logged-in sessions that may exist)
- open /login
-  enter test_user's email into element  `#email`
-  enter test_user's password into element  `#password`
-  click element  `input[type="submit"]`
- open /
- enter a test_tickets name into the sell form element `#name`
- enter a test_tickets quantity into the sell form element`#quantity`
- enter a test_tickets price into the sell form element `#price`
- enter a test_ticket expiration date into the sell form element `#expiration-date`
- click the element `input[type="submit"]`
- validate the current page contains the `#update-message`element `succesful`
