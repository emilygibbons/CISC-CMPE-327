
# Seet Geek Design Document
*Class and method descriptions.*

## Class Diagram
![alt text](https://github.com/emilygibbons/CISC-CMPE-327/blob/DesignDoc/pictures/MermaidDiagram_2.png)

## \_\_init\_\_

This class initializes the application and sets it up to run with Flask.

## \_\_main\_\_
The main class runs the server at a given port.

## Models
Creates all the SQL tables and also contains the **Ticket** and **User** classes.
### app.app_context()
Function is used to create all the SQL tables if they do not exist.

## User
User class holds the information for a user (ID, email, password, name, balance) and is used to access database.

## Ticket
Ticket class hold the information for a ticket (ID, name, price, date, email) and is used to access database.

## backend
Holds all of the backend logic that interacts with the database and other services.
### get_user()
Function is used to get user by a given email.
### login_user()
This function authenticates the user by comparing the username and password to the database.
### register_user()
Used to register a new user into the database.
### get_ticket()
Used to get a ticket from the database by its ID.
###  verify_ticket()
Verifies the ticket(s) exist in the database given its quantity, name, price, expiration date, and email
### get_all_tickets()
Used to get a list of all available tickets.
### sell_ticket()
Takes the information inputted in the form on the website assigns and adds it to the list
of available tickets in the data base
### buy_ticket()
Takes the information inputted in the form on the frontend and, deletes quantity amount
of tickets from the list of available tickets.
### getTicketsPrice()
Takes the information from the front end, and gets the overall price
of all the tickets looking to be purchased
### delete_ticket()
Takes the parameters and searches the database for a Ticket object that matches the email price and date and uses a for loop to delete in range quantity if multiple tickets exist, because quantity is not stored in a Ticket object.
### isEnoughTickets()
Verifies the amount of tickets are correct given the name and quantity
### ticketExists()
Verifies that the tickets exist in database given the name


## frontend
Defines the front-end part of the app, handles http requests.

### register_get()
Gets the viewing of the register page.
### register_post()
Takes the data entered by the user and validates it, then if possible registers user in database.
### login_get()
Gets the viewing of the login page.
### login_post()
Takes the data entered by the user and validates it, then if possible, sends user to home page.
### logout()
Logs the user out of the system.
### authenticate()
Authenticates that the user is able to enter a new homepage session.
### profile()
Gets all tickets from ticket list to be displayed on users homepage.
### sell_post()
Takes the data entered into the form and gets the email of the user and submits it to the backend to create a Ticket object with data entered as attributes.
### buy_post()
Takes the data entered into the form and submits it to the backend to delete a Ticket object, with the data entered in as attributes, from the database
### update_post()
Takes the data entered into the old ticket and new ticket form and deletes the Ticket(s) with the data entered into the old ticket form and creates new updated Ticket(s) from the data entered in the new ticket form
### error_404()
When the user tries to access a page that does not exist, creates an error message and renders the error html page and directs them to it
### checkEmailFormat()
Takes an email and compares it to a regex to see if it matches the standards.
### checkPasswordFormat()
Takes the users password and sees if it qualifies to be strong enough.
### checkUserNameFormat()
Makes sure that the username is alphanumeric, not too short or too long, and does not start or end with a space.
### checkTicketName() 
Makes sure the ticket is alphanumeric-only, no longer than 60 characters and does not start or end with a space.
### checkQuantity()
Makes sure the quantity of the tickets is more than 0, and less than or equal to 100.
### checkExpire()
Takes the expiration date and checks if it is not expired (date is not earlier than todays date).
### checkPrice()
Makes sure that price is 10 to 100
### checkDateFormat()
Takes the expiration date and checks if it meets the required 'YYYYMMDD' format.
### checkTicketExists()
Send ticket name to backend to see if it already exists
### hasEnoughBalance()
Checks if user has enough balance by taking the name of tickets being purchased and the amount, and compares on backend with the user balance the price of all the tickets combined including service charge as well as tax.


