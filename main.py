import os
from flask import Flask, render_template, request, jsonify

from modules import auth

app = Flask(__name__)

app.secret_key = os.environ['SESSION_SECRET_KEY']
auth.google_signin_key = os.environ['GOOGLE_SIGNIN_KEY']


@app.route('/')
def root():
    return render_template('index.html', gsignin_key=auth.google_signin_key)


@app.route('/get-user-data', methods=['GET'])
def get_user_data():
    user_info = auth.authenticate(request)
    if user_info:
        return render_template('partials/user_info.html', user_info=user_info)
    else:
        return jsonify({'message': 'error'}), 401


@app.route('/sign-out', methods=['GET'])
def sign_out():
    sign_out_request = auth.sing_out()

    if sign_out_request:
        return jsonify({'message': 'success'})
    else:
        return jsonify({'message': 'error'}), 400


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
