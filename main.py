import os

from flask import Flask, render_template, request, jsonify
from google.auth.transport import requests
from google.oauth2 import id_token

firebase_request_adapter = requests.Request()

app = Flask(__name__)
google_signin_key = os.environ['GOOGLE_SIGNIN_KEY']


@app.route('/')
def root():
    return render_template('index.html', gsignin_key=google_signin_key)


@app.route('/checktoken', methods=['POST'])
def check_token():
    try:
        token = request.form['token']
        idinfo = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            google_signin_key)

        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')

        userid = idinfo['sub']

        return jsonify(userid)

    except ValueError:
        return 'error', 401


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
