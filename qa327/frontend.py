from flask import render_template, request, session, redirect
from qa327 import app
import qa327.backend as bn
import re

"""
This file defines the front-end part of the service.
It elaborates how the services should handle different
http requests from the client (browser) through templating.
The html templates are stored in the 'templates' folder. 
"""


@app.route('/register', methods=['GET'])
def register_get():
    # templates are stored in the templates folder
    return render_template('register.html', message='')


@app.route('/register', methods=['POST'])
def register_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    error_message = None

    # checks validity of email and passwords
    if (not bn.checkEmailFormat(email)):
        error_message = "email format is incorrect."
    elif (not bn.checkUserNameFormat(name)):
        error_message = "username format incorrect."
    elif (not bn.checkPasswordFormat(password)):
        error_message = "password format (1) incorrect."
    elif (not bn.checkPasswordFormat(password2)):
        error_message = "password format (2) incorrect."
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
    if not bn.checkEmailFormat(email) or not bn.checkPasswordFormat(password):
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

    return render_template('index.html', user=user,tickets=tickets)

@app.route('/sell', methods=['POST'])
def sell_post():

    # Gets the information needed from the form to create the Ticket object. 
    email = session['logged_in']
    quantity = request.form.get('sell-quantity')
    name = request.form.get('sell-name')
    price = request.form.get('sell-price')
    date = request.form.get('sell-expiration-date')

    #submits the ticket into the database, which then displays in the available tickets.
  
    bn.sell_ticket(quantity,name,email,price,date)
    
    return redirect('/')    #redirects back to the users profile.

@app.route('/buy',methods=['POST'])
def buy_post():
    # Gets the information needed to "buy" the ticket. At this current stage it only deletes it for now..
 
    name = request.form.get('buy-name')
    quantity = request.form.get('buy-quantity')

    #evaulates which ticket you want to "buy" and deletes it from the database. 
    bn.buy_ticket(name,quantity)

    return redirect('/')     #redirects back to the users profile. 

@app.route('/update',methods=['POST'])
def update_post():
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

   # delete the old tickets and remake the new ones.

    bn.delete_ticket(quantity_old, name_old, price_old, expiration_date_old, email)

   #remake the requested new tickets.

    bn.sell_ticket(quantity_new, name_new,email, price_new, expiration_date_new)
    

    return redirect('/')

@app.errorhandler(404)
def error404(e):
    error_message = 'Error 404'
    return render_template('error.html', message=error_message)
