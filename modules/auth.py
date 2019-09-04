import os

from google.auth.transport import requests
from google.oauth2 import id_token

google_signin_key = os.environ['GOOGLE_SIGNIN_KEY']


def check_token(request):
    try:
        token = request.headers.get('X-User-Token')
        idinfo = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            google_signin_key)

        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')

        user_info = idinfo

        return user_info

    except ValueError:
        return False
