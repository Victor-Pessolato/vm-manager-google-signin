from modules import auth

from flask import Flask, render_template, request, jsonify, session
from flask_session import Session

app = Flask(__name__)

# Set the configuration for a server-side session
app.config.from_object(__name__)
Session(app)


@app.route('/')
def root():
    return render_template('index.html', gsignin_key=auth.google_signin_key)


@app.route('/get-user-data', methods=['GET'])
def get_user_data():
    user_info = auth.check_token(request)
    if user_info:
        return render_template('partials/user_info.html', user_info=user_info)
    else:
        return jsonify({'message': 'error'}), 401


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
