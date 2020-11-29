# Test Case R6
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
### Test Case R6.1 -   The name of the ticket has to be alphanumeric-only, and space allowed only if it is not the first or the last character -Negative case
Mocking:

-   Mock backend.get_user to return a test_user instance
-   Mock backend.get_ticket to return a test_ticket instance

Actions:

-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   enter test_user's email into element  `#email`
-   enter test_user's password into element  `#password`
-   click element  `input[type="submit"]`
-   open /
-   enter  `(pretend this is a space) ticket_no_existo`  into element  `#buy_name`
-   enter test_ticket's quantity into element  `#buy_quantity`
-   click element  `input[type="submit"]`
-   validate that the  `#buy_message`  element shows  `Error:Ticket name cannot have a space at the begining.`

### Test Case R6.1 -   The name of the ticket has to be alphanumeric-only, and space allowed only if it is not the first or the last character -Positive Case 
Mocking:

-   Mock backend.get_user to return a test_user instance
-   Mock backend.get_ticket to return a test_ticket instance

Actions:

-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   enter test_user's email into element  `#email`
-   enter test_user's password into element  `#password`
-   click element  `input[type="submit"]`
-   open /
-   enter  test_tickets name   into element  `#buy_name`
-   enter test_ticket's quantity into element  `#buy_quantity`
-   click element  `input[type="submit"]`
-   validate that the  `#buy_message`  element shows  `succesful`

### Test Case R6.2 - The name of the ticket is no longer than 60 characters- Positive Case
Mocking:

-   Mock backend.get_user to return a test_user instance
-   Mock backend.get_ticket to return a test_ticket instance

Actions:

-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   enter test_user's email into element  `#email`
-   enter test_user's password into element  `#password`
-   click element  `input[type="submit"]`
-   open /
-   enter test_ticket's name into element  `#buy_name`
-   enter test_ticket's quantity into element  `#buy_quantity`
-   click element  `#buy_submit`
-   validate that the  `#buy_message` element shows  `successful`

### Test Case R6.2 - The name of the ticket is no longer than 60 characters- Negative Case
Mocking:

-   Mock backend.get_user to return a test_user instance
-   Mock backend.get_ticket to return a test_ticket instance

Actions:

-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   enter test_user's email into element  `#email`
-   enter test_user's password into element  `#password`
-   click element  `input[type="submit"]`
-   open /
-   enter  `IAmLongerThan60Charactersbelieveme..........................`  into element  `#sell_name`
-   enter test_ticket's quantity into element  `#buy_quantity`
-   click element  `#buy_submit``
-   validate that the   `#buy_message`  element shows  `Error:Ticket name can not be longer than 60 characters`

### Test Case R6.3 - The quantity of the tickets has to be more than 0, and less than or equal to 100  -Positive Case
Mocking:

-   Mock backend.get_user to return a test_user instance
-   Mock backend.get_ticket to return a test_ticket instance

Actions:
-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   enter test_user's email into element  `#email`
-   enter test_user's password into element  `#password`
-   click element  `input[type="submit"]`
-   open /
-   enter test_ticket's name into element  `#buy_name`
-   enter test_ticket's quantity into element  `#buy_quantity`
-   click element  `#buy_submit`
-   validate that the  `#buy_message`  element shows  `successful`

### Test Case R6.3 - The quantity of the tickets has to be more than 0, and less than or equal to 100  -Negative Case
Mocking:

-   Mock backend.get_user to return a test_user instance
-   Mock backend.get_all_tickets to return a test_tickets instance

Actions:

-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   enter test_user's email into element  `#email`
-   enter test_user's password into element  `#password`
-   click element  `input[type="submit"]`
-   open /
-   enter test_ticket's name into element  `#buy_name`
-   enter  `1337`  into element  `#buy_quantity`
-   click element  `#buy_submit`
-   validate that the  `#buy_message`  element shows  `Error:Quantity of tickets needs to be min:1 max:100`

### Test Case R6.4 - The ticket name exists in the database and the quantity is more than the quantity requested to buy - Positive Case

Mocking:

-   Mock backend.get_user to return a test_user instance
-   Mock backend.get_ticket to return a test_ticket instance

Actions:
-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   enter test_user's email into element  `#email`
-   enter test_user's password into element  `#password`
-   click element  `input[type="submit"]`
-   open /
-   enter test_ticket's name into element  `#buy_name`
-   enter test_ticket's quantity into element  `#buy_quantity`
-   click element  `#buy_submit`
-   validate that the  `#buy_message`  element shows  `successful`

### Test Case R6.4 - The ticket name exists in the database and the quantity is more than the quantity requested to buy -Name does not exist.
Mocking:

-   Mock backend.get_user to return a test_user instance
-   Mock backend.get_ticket to return a test_ticket instance

Actions:
-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   enter test_user's email into element  `#email`
-   enter test_user's password into element  `#password`
-   click element  `input[type="submit"]`
-   open /
-   enter  `fakenamethatdoesnotexistindatabase` into element  `#buy_name`
-   enter test_ticket's quantity into element  `#buy_quantity`
-   click element  `#buy_submit`
-   validate that the  `#buy_message`  element shows  `Error: Ticket does not exist.`

### Test Case R6.4 - The ticket name exists in the database and the quantity is more than the quantity requested to buy -Quanity requested is more than in stock case
Mocking:

-   Mock backend.get_user to return a test_user instance
-   Mock backend.get_ticket to return a test_ticket instance

Actions:
-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   enter test_user's email into element  `#email`
-   enter test_user's password into element  `#password`
-   click element  `input[type="submit"]`
-   open /
-   enter test_ticket's name into element  `#buy_name`
-   enter `anamountlongerthaninstock` into element  `#buy_quantity`
-   click element  `#buy_submit`
-   validate that the  `#buy_message`  element shows  `Error: The quantity of tickets requested is not available.`

### Test Case R6.5 - The user has more balance than the ticket price * quantity + service fee (35%) + tax (5%) - Positive case

Mocking:

-   Mock backend.get_user to return a test_user instance
-   Mock backend.get_ticket to return a test_ticket instance

Actions:
-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   enter test_user's email into element  `#email`
-   enter test_user's password into element  `#password`
-   click element  `input[type="submit"]`
-   open /
-   enter test_ticket's name into element  `#buy_name`
-   enter test_ticket's quantity into element  `#buy_quantity`
-   click element  `#buy_submit`
-   validate that the  `#buy_message`  element shows  `successful`

### Test Case R6.5 - The user has more balance than the ticket price * quantity + service fee (35%) + tax (5%) -Negative case
Mocking:

-   Mock backend.get_user to return a test_user instance
-   Mock backend.get_ticket to return a test_ticket instance

Actions:
-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   enter test_user's email into element  `#email`
-   enter test_user's password into element  `#password`
-   click element  `input[type="submit"]`
-   open /
-   enter test_ticket's name into element  `#buy_name`
-   enter test_ticket's quantity into element  `#buy_quantity`
-   click element  `#buy_submit`
-   validate that the  `#buy_message`  element shows  `Error: Users Balance has insufficent funds for this purchase.``

### Test Case R6.6 - For any errors, redirect back to / and show an error message.
Mocking:

-   Mock backend.get_user to return a test_user instance
-   Mock backend.get_ticket to return a test_ticket instance

Actions:

-   open /logout (to invalidate any logged-in sessions that may exist)
-   enter  `ticketthatdoesntexist`  name into element  `#buy_name`
-   enter  `1337`  into element  `#buy_quantity`
-   click element  `#buy_submit`
-   validate that  `#buy-message`  element shows  `Error: An error has occured. Please try again later.`
-   open /
-   validate that current page contains  `#welcome-header`  element
-   validate that  `#error-message`  says  `There was a error entering your ticket.`

