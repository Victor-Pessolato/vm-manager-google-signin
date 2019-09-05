from flask import session
from google.auth.transport import requests
from google.oauth2 import id_token
from google.cloud import datastore

google_signin_key = None

client = datastore.Client()


def identify(token):
    idinfo = id_token.verify_oauth2_token(
                token,
                requests.Request(),
                google_signin_key)

    if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
        raise ValueError('Wrong issuer.')

    return idinfo


def authorize(user_data):
    query = client.query(kind='AllowedUsers')
    query.projection = ['email']
    allowed_users = list(query.fetch())
    print(allowed_users)
    """
    key = client.key('User', user_data['email'])
    is_allowed = client.get(key)

    if is_allowed:
        return True
    else:
        return False
    """
    return user_data


def authenticate(request):
    try:
        user_session = session.get('user_info', None)
        # If user session is still open, we ignore the token sent.
        if user_session:
            user_info = user_session
        else:
            # If there is no user session, we check if the token is from a valid user.
            token = request.headers.get('X-User-Token')
            user_info = identify(token)
            session['user_info'] = user_info

        return authorize(user_info)

    except ValueError:
        return False
