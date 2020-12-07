from flask import render_template, request, session, redirect
from qa327 import app
import qa327.backend as bn
import re
import datetime

"""
This file defines the front-end part of the service.
It elaborates how the services should handle different
http requests from the client (browser) through templating.
The html templates are stored in the 'templates' folder. 
"""


@app.route('/register', methods=['GET'])
def register_get():
    # templates are stored in the templates folder
    return render_template('register.html', message='Please enter info below')


@app.route('/register', methods=['POST'])
def register_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    error_message = None

    # checks validity of email and passwords
    if (not checkEmailFormat(email)):
        error_message = "email format is incorrect."
    elif (not checkUserNameFormat(name)):
        error_message = "username format incorrect."
    elif (not checkPasswordFormat(password)):
        error_message = "password format incorrect."
    elif (not checkPasswordFormat(password2)):
        error_message = "password format incorrect."
    elif (password != password2):
        error_message = "passwords not equal"
    else:
        user = bn.get_user(email)
        if user:
            error_message = "this email has been ALREADY used"
        elif not bn.register_user(email, name, password, password2, 5000.00):
            error_message = "Failed to store user info."

    # if there is any error messages when registering new user
    # at the backend, go back to the register page.
    if error_message:
        return render_template('register.html', message=error_message)
    else:
        return redirect('/login')


@app.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html', message='Please login')


@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    user = bn.login_user(email, password)
    error_message = None

    # checks that email and password format are correct
    if not checkEmailFormat(email) or not checkPasswordFormat(password):
        error_message = "email/password format is incorrect."

    if error_message:
        return render_template('login.html', message=error_message)
    elif user:
        session['logged_in'] = user.email
        """
        Session is an object that contains sharing information 
        between browser and the end server. Typically it is encrypted 
        and stored in the browser cookies. They will be past 
        along between every request the browser made to this services.

        Here we store the user object into the session, so we can tell
        if the client has already login in the following sessions.

        """
        # success! go back to the home page
        # code 303 is to force a 'GET' request
        return redirect('/', code=303)
    else:
        return render_template('login.html', message='email/password combination incorrect')


@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in', None)
    return redirect('/')


def authenticate(inner_function):
    """
    :param inner_function: any python function that accepts a user object

    Wrap any python function and check the current session to see if 
    the user has logged in. If login, it will call the inner_function
    with the logged in user object.

    To wrap a function, we can put a decoration on that function.
    Example:

    @authenticate
    def home_page(user):
        pass
    """

    def wrapped_inner():

        # check did we store the key in the session
        if 'logged_in' in session:
            email = session['logged_in']
            user = bn.get_user(email)
            if user:
                # if the user exists, call the inner_function
                # with user as parameter
                return inner_function(user)
        else:
            # else, redirect to the login page

            return redirect('/login')
    # Added this statement because i was getting an Assertion Error
    wrapped_inner.__name__ = inner_function.__name__
    # return the wrapped version of the inner_function:
    return wrapped_inner


@app.route('/')
@authenticate
def profile(user):
    # authentication is done in the wrapper function
    # see above.
    # by using @authenticate, we don't need to re-write
    # the login checking code all the time for other
    # front-end portals
    tickets = bn.get_all_tickets()

    return render_template('index.html', user=user, tickets=tickets, message='')


@app.route('/sell', methods=['POST'])
@authenticate
def sell_post(user):

    statusMessage = ''
    # Gets the information needed from the form to create the Ticket object.

    email = session['logged_in']
    quantity = request.form.get('sell-quantity')
    name = request.form.get('sell-name')
    price = request.form.get('sell-price')
    date = request.form.get('sell-expiration-date')

    # checks validity of the parameters specified requirements for 'sell'.

    if not(checkQuantity(quantity)):
        statusMessage = "Error: The quantity of the tickets has to be between 1 and 100."

    elif not(checkTicketName(name)):
        statusMessage = "Error: The name has to alphanumeric, have no spaces in the beginning or end and be between 6 and 60 characters."
    elif not(checkDateFormat(date)):
        statusMessage = "Error: The date has to be in the format 'YYYYMMDD'."

    elif not(checkExpire(date)):
        statusMessage = "Error: The date cannot be expired."

    elif not(checkPrice(price)):
        statusMessage = "Error: The price has to be between $10 and $100."

    if statusMessage != '':
        tickets = bn.get_all_tickets()
        return render_template('index.html', user=user, tickets=tickets, sellMessage=statusMessage)
    else:
        # submits the ticket into the database, which then displays in the available tickets.
        bn.sell_ticket(quantity, name, email, price, date)
        # updates tickets.
        tickets = bn.get_all_tickets()
        return render_template('index.html', user=user, tickets=tickets, sellMessage='Listing posted successful')


@app.route('/buy', methods=['POST'])
@authenticate
def buy_post(user):

    statusMessage = ''
    # Gets the information needed from the form to create the Ticket object.

    email = session['logged_in']
    quantity = request.form.get('buy-quantity')
    name = request.form.get('buy-name')

    if (checkTicketExists(name)):

        if not(checkTicketName(name)):
            statusMessage = "Error: The name has to alphanumeric, have no spaces in the beginning or end and be between 6 and 60 characters."
        elif not(checkQuantity(quantity)):
            statusMessage = "Error: The quantity of the tickets has to be between 1 and 100."
        elif not(bn.isEnoughTickets(name, quantity)):
            statusMessage = "Error: The specified quantity of tickets not available."
        elif not (hasEnoughBalance(user, name, quantity)):
            statusMessage = "Error: Your balance is too low!"

        if statusMessage != '':
            tickets = bn.get_all_tickets()
            return render_template('index.html', user=user, tickets=tickets, buyMessage=statusMessage)
        else:
            # evaulates which ticket you want to "buy" and deletes it from the database.
            bn.buy_ticket(name, quantity)

            tickets = bn.get_all_tickets()
            return render_template('index.html', user=user, tickets=tickets, buyMessage='Purchase successful')
    else:
        statusMessage = "Ticket does not exist."
        tickets = bn.get_all_tickets()
        return render_template('index.html', user=user, tickets=tickets, buyMessage=statusMessage)


@app.route('/update', methods=['POST'])
@authenticate
def update_post(user):
    statusMessage = ''

    email = session['logged_in']
    quantity_old = request.form.get('quantity-old')
    name_old = request.form.get('name-old')
    price_old = request.form.get('price-old')
    expiration_date_old = request.form.get('expiration-date-old')

    # New update changes.
    quantity_new = request.form.get('quantity-new')
    name_new = request.form.get('name-new')
    price_new = request.form.get('price-new')
    expiration_date_new = request.form.get('expiration-date-new')

    # Checking validity of the 'new' parameters.
    if not(checkTicketName(name_new)):
        statusMessage = "Error: The updated name has to alphanumeric, have no spaces in the begining or end and be between 6 and 60 characters."

    elif not(checkQuantity(quantity_new)):
        statusMessage = "Error: The updated quantity of tickets needs to be between 1 and 100."

    elif not(checkPrice(price_new)):
        statusMessage = "Error: The updated price needs to be between $10 and $100."

    elif not(checkDateFormat(expiration_date_new)):
        statusMessage = "Error: The updated exipiration date needs to be follow the 'YYYYMMDD' format."

    elif not(checkExpire(expiration_date_new)):
        statusMessage = "Error: The updated exipiration date cannot be expired."

    elif not(bn.verify_ticket(quantity_old, name_old, price_old, expiration_date_old, email)):
        statusMessage = "Error: The entered ticket either does not exist or was entered incorrectly, please try again."

    if statusMessage != '':
        tickets = bn.get_all_tickets()
        return render_template('index.html', user=user, tickets=tickets, updateMessage=statusMessage)
    else:
        # deletes old ticket(s).
        bn.delete_ticket(quantity_old, name_old, price_old,
                         expiration_date_old, email)
        # submits new ticket(s) to the database.
        bn.sell_ticket(quantity_new, name_new, email,
                       price_new, expiration_date_new)
        # updates the ticket list.
        tickets = bn.get_all_tickets()
        return render_template('index.html', user=user, tickets=tickets, updateMessage='Listing update successful')


@app.errorhandler(404)
def error404(e):
    error_message = 'Error 404'
    return render_template('error.html', message=error_message)


def checkEmailFormat(email):
    """
    :param email: users entered email

    Take the email are run it through a regex to see if it meets specifications.
    If it does then return true, if it doesnt then return false.
    """

    if re.match("[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?", email, re.IGNORECASE):
        return True
    else:
        return False


def checkPasswordFormat(password):
    """
    :param password: users entered password

    Take the password are run it through a regex to see if it meets specifications.
    If it does then return true, if it doesnt then return false.
    """

    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"

    # compiling regex

    pat = re.compile(reg)

    # searching regex

    mat = re.search(pat, password)

    # validating conditions

    if mat:
        return True
    else:
        return False


def checkUserNameFormat(u):
    """
    :param u: users entered username

    Take the user are run it through a regex to see if it meets specifications.
    Also checks that the username does not start or end with a space
    If it does then return true, if it doesnt then return false.
    """
    if bool(re.match('^[a-zA-Z0-9]+$', u)) and (2 < len(u) < 20) and not u.startswith(" ") and not u.endswith(" "):
        return True
    else:
        return False

# For R4, R5, R6


def checkTicketName(t):
    """
    :param t: user entered ticket

    Takes the ticket and runs it through a regex to see if it meets the required specifications.
    Also checks that the ticket does not start or end with a space
    If it does then return true, if it does not then return false.
    """
    if bool(re.match('^[a-zA-Z0-9" "]+$', t) and (6 <= len(t) <= 60) and not t.startswith(" ") and not t.endswith(" ")):
        return True
    else:
        return False

# For R4, R5, R6


def checkQuantity(q):
    """
    :param q: users entered quantity

    Takes the quantity and checks if it meets the required specifications.
    If it does then return true, if it doesnt then return false.
    """
    if bool(0 < int(q) <= 100):
        return True
    else:
        return False

# For R4, R5


def checkExpire(e):
    """
    :param e: users entered expiration date

    Takes the expiration date and checks if it is not expired.
    If it does then return true, if it doesnt then return false.
    """
    try:
        if(datetime.datetime.now() < datetime.datetime.strptime(e, '%Y%m%d')):
            return True
        else:
            return False

    except ValueError:
        return False
# For R4, R5


def checkPrice(p):
    """
    :param p: users entered price

    Takes the expiration date and checks if it meets the required specifications.
    If it does then return true, if it does not they return false.
    """
    if (10 <= int(p) <= 100):
        return True
    else:
        return False
# For R4, R5


def checkDateFormat(d):
    """
    :param d: users entered expiration date

    Takes the expiration date and checks if it meets the required 'YYYYMMDD' format.
    If it does then return true, if it doesnt then return false.
    """
    try:
        if(len(d) == 8):
            datetime.datetime.strptime(d, '%Y%m%d')
            return True
        else:
            return False
    except ValueError:
        return False


def checkTicketExists(name):
    """
    :param name: takes ticket name

    gets tickets name and then calls function on backend that will return
    boolean based on whether the ticket exists or not
    """
    return bn.ticketExists(name)


def hasEnoughBalance(user, name, quantity):
    """ 
    :param user: user instance
    :param name: name of ticket
    :param quantitiy: amount of tickers

    takes the name of tickets being purchased and the amount, calls funtion on backend
    that returns the price of all the tickets combined. Then compares the users balance
    to the price of all of the combined tickets including service charge as well as tax.
    If the user has enough balance then return true, if not then return false.
    """

    balance = user.balance
    price = bn.getTicketsPrice(name, quantity)
    price = round(((price*1.35)*1.05), 2)

    if price > balance:
        return False
    else:
        user.balance = user.balance-price
        return True
