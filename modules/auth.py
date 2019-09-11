from flask import session
from google.auth.transport import requests
from google.oauth2 import id_token

from modules import db_manager

google_signin_key = None


def identify(token):
    idinfo = id_token.verify_oauth2_token(
                token,
                requests.Request(),
                google_signin_key)

    allowed_types = ['accounts.google.com', 'https://accounts.google.com']
    if idinfo['iss'] not in allowed_types:
        raise ValueError('Wrong issuer.')

    return idinfo


def authorize(user_info):
    is_allowed = db_manager.is_allowed(user_info['email'])

    if is_allowed:
        return user_info
    else:
        return False


def authenticate(request):
    try:
        user_session = session.get('user_info', None)
        # If user session is still open, we ignore the token sent.
        if user_session:
            user_info = user_session
        else:
            # If there is no user session,
            # we check if the token is from a valid user.
            token = request.headers.get('X-User-Token')

            # Here we look for the user's identity
            user_info = identify(token)

            # We store user's info in the session
            session['user_info'] = user_info

        # We store is in the DB
        db_manager.store_visitor(user_info)
        # And checks if user is authorized to proceed
        return authorize(user_info)

    except ValueError:
        return False


def sing_out():
    try:
        session.pop('user_info', None)
        return True
    except ValueError:
        return False
