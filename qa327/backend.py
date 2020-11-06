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
    new_user = User(email=email, name=name, password=hashed_pw, balance=balance)

    db.session.add(new_user)
    db.session.commit()
    return True


def get_ticket(id):
    """
    Get a ticket by a given id
    :param id: the id of the ticket
    :return: a ticket that has the matched ticket id
    """
    ticket = ticket.query.filter_by(id=id).first()
    return ticket


def get_all_tickets():
    return []

def checkEmailFormat(email):
    """
    :param email: users entered email

    Take the email are run it through a regex to see if it meets specifications.
    If it does then return true, if it doesnt then return false.
    """

    if re.match("\A(?P<name>[\w\-_]+)@(?P<domain>[\w\-_]+).(?P<toplevel>[\w]+)\Z", email, re.IGNORECASE):
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
