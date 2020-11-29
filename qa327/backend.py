from qa327.models import db, User, Ticket
from werkzeug.security import generate_password_hash, check_password_hash
import re

"""
This file defines all backend logic that interacts with database and other services
"""


def get_user(email):
    """
    Get a user by a given email
    :param email: the email of the user
    :return: a user that has the matched email address
    """
    user = User.query.filter_by(email=email).first()
    return user


def login_user(email, password):
    """
    Check user authentication by comparing the password
    :param email: the email of the user
    :param password: the password input
    :return: the user if login succeeds
    """
    # if this returns a user, then the name already exists in database
    user = get_user(email)
    if not user or not check_password_hash(user.password, password):
        return None
    return user


def register_user(email, name, password, password2, balance):
    """
    Register the user to the database
    :param email: the email of the user
    :param name: the name of the user
    :param password: the password of user
    :param password2: another password input to make sure the input is correct
    :return: an error message if there is any, or None if register succeeds
    """
    hashed_pw = generate_password_hash(password, method='sha256')
    # store the encrypted password rather than the plain password
    new_user = User(email=email, name=name,
                    password=hashed_pw, balance=balance)

    db.session.add(new_user)
    db.session.commit()
    return True


def get_ticket(id):
    """
    Get a ticket by a given id
    :param id: the id of the ticket
    :return: a ticket that has the matched ticket id
    """
    ticket = Ticket.query.filter_by(id=id).first()
    return ticket


def verify_ticket(quantity, name, price, expiration_date, email):
    """
    Verifies the ticket(s) exist in the database by the given parameters
    :param quantity: the quantity of the ticket
    :return: a ticket that has the matched ticket id
    """
    tickets = Ticket.query.filter_by(
        name=name, price=price, date=expiration_date, email=email).all()
    if len(tickets) == int(quantity):
        return True
    else:
        return False


def get_all_tickets():
    """"
    Returns all tickets available to be purchased.
    """

    tickets = Ticket.query.all()

    return tickets


def sell_ticket(quantity, name, email, price, expiration_date):
    """
    :Param quantity: Quantity of tickets that are being sold.
    :Param name: The name of the ticket.
    :Param email: The owners email that is selling the ticket.
    :Param price: The price of the ticket being sold.
    :Param expiration date: The date the ticket expires.

    Takes the information inputed in the form on the website assigns and adds it to the list
    of available tickets in the data base.
    """
    for i in range(int(quantity)):
        new_ticket = Ticket(name=name, email=email,
                            price=price, date=expiration_date)
        db.session.add(new_ticket)
        db.session.commit()
    return True


def buy_ticket(name, quantity):
    """
    :Param quantity: Quantity of tickets that are being bought.
    :Param name: The name of the ticket that is being bought.

    Takes the information inputed in the form on the frontend and,for now, deletes quantity amount
    of tickets from the list of available tickets.
    """

    for i in range(int(quantity)):
        ticket = Ticket.query.filter_by(name=name).first()
        db.session.delete(ticket)
        db.session.commit()
    return True

def getTicketsPrice(name, quantity):
    price = 0

    for i in range(int(quantity)):
        ticket = Ticket.query.filter_by(name=name).first()
        price += ticket.price

    return price


def delete_ticket(quantity, name, price, expiration, email):
    """
    :Param quantity: Quantity of tickets that are being sold.
    :Param name: The name of the ticket.
    :Param email: The owners email that is selling the ticket.
    :Param price: The price of the ticket being sold.
    :Param expiration date: The date the ticket expires.

    Takes the params and searches the database for a Ticket object that matches the email price and date.
    Uses a for loop to delete in range quantity if multiple tickets exist, because quantity is not stored as
    in a Ticket object.
    """

    for i in range(int(quantity)):
        ticket = Ticket.query.filter_by(
            name=name, price=price, date=expiration, email=email).first()
        db.session.delete(ticket)
        db.session.commit()
    return True


def isEnoughTickets(name, quantity):
    """
    Verifies the amount of tickets are correct
    :param quantity: the quantity of the ticket
    :return: true or false
    """
    tickets = Ticket.query.filter_by(name=name).all()
    if len(tickets) >= int(quantity):
        return True
    else:
        return False

def ticketExists(name):
    tickets = Ticket.query.filter_by(name=name).all()

    if tickets:
        return True
    else:
        return False
