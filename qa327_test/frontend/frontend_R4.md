# Test Case R4 /sell
Test data:
```
test_ticket = Ticket(
	owner='test_frontend@test.com',
    name='test_ticket',
    price=99,
    date='20200901
    quantity='69'
)
```
## [GET]
#### Test Case R4.1 - The name of the ticket has to be alphanumeric-only, and space allowed only if it is not the first or the last character. - Positive
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
-   enter test_ticket's name into element  `#sell_name`
-   enter test_ticket's quantity into element  `#sell_quantity`
-   enter test_ticket's sell price into element `#sell_price`
- enter test_tickets date into element `#sell_date`
-   click element  `#sell_submit`
-   validate that the  `#sell_message`  element shows  `successful`
-   open /logout (clean up)

#### Test Case R4.1 - The name of the ticket has to be alphanumeric-only, and space allowed only if it is not the first or the last character. - Negative
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
-   enter `(pretend this is a space) ticket_no_existo` into element  `#sell_name`
-   enter test_ticket's quantity into element  `#sell_quantity`
-   enter test_ticket's sell price into element `#sell_price`
- enter test_tickets date into element `#sell_date`
-   click element  `#sell_submit`
-   validate that the  `#sell_message`  element shows  `ticket name format not allowed`
-   open /logout (clean up)

#### Test Case R4.2 - The name of the ticket is no longer than 60 characters - Positive
Mocking:
-   Mock backend.get_user to return a test_user instance
-   Mock backend.get_ticket to return a test_ticket instance

Actions:
-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   enter test_user's email into element  `#email`
-   enter test_user's password into element  `#password`
-   click element  `input[type="submit"]`
-   open /
-   enter test_ticket's name into element  `#sell_name`
-   enter test_ticket's quantity into element  `#sell_quantity`
-   enter test_ticket's sell price into element `#sell_price`
- enter test_tickets date into element `#sell_date`
-   click element  `#sell_submit`
-   validate that the  `#sell_message`  element shows  `successful`
-   open /logout (clean up)

#### Test Case R4.2 - The name of the ticket is no longer than 60 characters - Negative
Mocking:
-   Mock backend.get_user to return a test_user instance
-   Mock backend.get_ticket to return a test_ticket instance

Actions:
-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   enter test_user's email into element  `#email`
-   enter test_user's password into element  `#password`
-   click element  `input[type="submit"]`
-   open /
-   enter `IAmLongerThan60CharactersHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHA` into element  `#sell_name`
-   enter test_ticket's quantity into element  `#sell_quantity`
-   enter test_ticket's sell price into element `#sell_price`
- enter test_tickets date into element `#sell_date`
-   click element  `#sell_submit`
-   validate that the  `#sell_message`  element shows  `ticket name format not allowed`
-   open /logout (clean up)

#### Test Case R4.3 - The quantity of the tickets has to be more than 0, and less than or equal to 100 - Positive
Mocking:
-   Mock backend.get_user to return a test_user instance
-   Mock backend.get_ticket to return a test_ticket instance

Actions:
-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   enter test_user's email into element  `#email`
-   enter test_user's password into element  `#password`
-   click element  `input[type="submit"]`
-   open /
-   enter test_ticket's name into element  `#sell_name`
-   enter test_ticket's quantity into element  `#sell_quantity`
-   enter test_ticket's sell price into element `#sell_price`
- enter test_tickets date into element `#sell_date`
-   click element  `#sell_submit`
-   validate that the  `#sell_message`  element shows  `successful`
-   open /logout (clean up)

#### Test Case R4.3 - The quantity of the tickets has to be more than 0, and less than or equal to 100 - Negative
Mocking:
-   Mock backend.get_user to return a test_user instance
-   Mock backend.get_all_tickets to return a test_tickets instance

Actions:
-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   enter test_user's email into element  `#email`
-   enter test_user's password into element  `#password`
-   click element  `input[type="submit"]`
-   open /
-   enter test_ticket's name into element  `#sell_name`
-   enter `6969` into element  `#sell_quantity`
-   enter test_ticket's sell price into element `#sell_price`
- enter test_tickets date into element `#sell_date`
-   click element  `#sell_submit`
-   validate that the  `#sell_message`  element shows  `Quantity of tickets needs to be min:1 max:100`
-   open /logout (clean up)

#### Test Case R4.4 - Price has to be of range [10, 100] - Positive

Mocking:
-   Mock backend.get_user to return a test_user instance
-   Mock backend.get_ticket to return a test_ticket instance

Actions:
-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   enter test_user's email into element  `#email`
-   enter test_user's password into element  `#password`
-   click element  `input[type="submit"]`
-   open /
-   enter test_ticket's name into element  `#sell_name`
-   enter test_ticket's quantity into element  `#sell_quantity`
-   enter test_ticket's sell price into element `#sell_price`
- enter test_tickets date into element `#sell_date`
-   click element  `#sell_submit`
-   validate that the  `#sell_message`  element shows  `successful`
-   open /logout (clean up)

#### Test Case R4.4 - Price has to be of range [10, 100] - Negative

Mocking:
-   Mock backend.get_user to return a test_user instance
-   Mock backend.get_ticket to return a test_ticket instance

Actions:
-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   enter test_user's email into element  `#email`
-   enter test_user's password into element  `#password`
-   click element  `input[type="submit"]`
-   open /
-   enter test_ticket's name into element  `#sell_name`
-   enter test_ticket's quantity into element  `#sell_quantity`
-   enter `99999999969` into element `#sell_price`
- enter test_tickets date into element `#sell_date`
-   click element  `#sell_submit`
-   validate that the  `#sell_message`  element shows  `sell price needs tp be min:10 max:100`
-   open /logout (clean up)


#### Test Case R4.5 - Date must be given in the format YYYYMMDD - Positive

Mocking:
-   Mock backend.get_user to return a test_user instance
-   Mock backend.get_ticket to return a test_ticket instance

Actions:
-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   enter test_user's email into element  `#email`
-   enter test_user's password into element  `#password`
-   click element  `input[type="submit"]`
-   open /
-   enter test_ticket's name into element  `#sell_name`
-   enter test_ticket's quantity into element  `#sell_quantity`
-   enter test_tickets price into element `#sell_price`
- enter test_tickets date into element `#sell_date`
-   click element  `#sell_submit`
-   validate that the  `#sell_message`  element shows  `successful`
-   open /logout (clean up)

#### Test Case R4.5 - Date must be given in the format YYYYMMDD - Negative

Mocking:
-   Mock backend.get_user to return a test_user instance
-   Mock backend.get_ticket to return a test_ticket instance

Actions:
-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   enter test_user's email into element  `#email`
-   enter test_user's password into element  `#password`
-   click element  `input[type="submit"]`
-   open /
-   enter test_ticket's name into element  `#sell_name`
-   enter test_ticket's quantity into element  `#sell_quantity`
-   enter test_tickets price into element `#sell_price`
-   enter `9000000000` into element `#sell_date`
-   click element  `#sell_submit`
-   validate that the  `#sell_message`  element shows  `Improper date format, date must be: YYYYMMDD`
-   open /logout (clean up)

#### Test Case R4.6 - For any errors, redirect back to / and show an error message
Mocking:
-   Mock backend.get_user to return a test_user instance
-   Mock backend.get_ticket to return a test_ticket instance

Actions:
-   open /logout (to invalidate any logged-in sessions that may exist)
-   enter `im_not_having_fun:/` name into element  `#sell_name`
-   enter `6777` into element  `#sell_quantity`
-   enter `-42` into element `#sell_price`
-   enter `9000000000` into element `#sell_date`
-   click element  `#sell_submit`
- validate that `#sell-message` element shows `error`
- open /
-   validate that current page contains  `#welcome-header`  element
- validate that `#error-message` says `There was a error entering your ticket`
-   open /logout (clean up)

#### Test Case R4.7 - The added new ticket information will be posted on the user profile page

Mocking:
-   Mock backend.get_user to return a test_user instance
-   Mock backend.get_ticket to return a test_ticket instance
- 
Actions:
-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /logout (to invalidate any logged-in sessions that may exist)
-   open /login
-   enter test_user's email into element  `#email`
-   enter test_user's password into element  `#password`
-   click element  `input[type="submit"]`
-   open /
-   enter test_ticket's name into element  `#sell_name`
-   enter test_ticket's quantity into element  `#sell_quantity`
-   enter test_ticket's sell price into element `#sell_price`
- enter test_tickets date into element `#sell_date`
-   click element  `#sell_submit`
-   validate that the  `#sell_message`  element shows  `successful`
- validate `/` page conatins  `#ticket_name`
-   open /logout (clean up)
