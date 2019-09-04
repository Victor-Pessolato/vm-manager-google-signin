from flask import session
from google.auth.transport import requests
from google.oauth2 import id_token

google_signin_key = None


def identify(token):
    idinfo = id_token.verify_oauth2_token(
                token,
                requests.Request(),
                google_signin_key)

    if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
        raise ValueError('Wrong issuer.')

    return idinfo


def authenticate(request):
    try:
        user_session = session.get('user_info', None)
        print(user_session)
        # If user session is still open, we ignore the token sent.
        if user_session:
            user_info = user_session
        else:
            # If there is no user session, we check if the token is from a valid user.
            token = request.headers.get('X-User-Token')
            user_info = identify(token)
            session['user_info'] = user_info

        return user_info

    except ValueError:
        return False
