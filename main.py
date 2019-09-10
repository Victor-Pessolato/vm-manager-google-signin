import os
from flask import Flask, render_template, request, jsonify

from modules import auth, compute

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


@app.route('/zones', methods=['GET'])
def get_zones():
    user_info = auth.authenticate(request)
    if user_info:
        # zones = compute.list_zones()
        # Uncomment in case I want to check for all the zones
        zones = [{'name': 'us-central1-a'}]
        zone_count = len(zones)
        return jsonify({'zones': zones, 'zone_count': zone_count})
    else:
        return jsonify({'message': 'error'}), 401


@app.route('/instances/<zone>', methods=['GET'])
def get_instances(zone):
    user_info = auth.authenticate(request)
    if user_info:
        instances = compute.list_instances(zone)

        if instances:
            # print(instances[0])
            return render_template(
                'partials/instances.html', instances=instances, zone=zone)
        else:
            return jsonify({'message': 'empty zone'})
    else:
        return jsonify({'message': 'error'}), 401


@app.route('/instances/<instance>/<action>', methods=['GET'])
def update_instance(instance, action):
    user_info = auth.authenticate(request)
    if user_info:
        if action == 'start':
            return jsonify(compute.start_vm('us-central1-a', instance))
        else:
            return jsonify(compute.stop_vm('us-central1-a', instance))

    else:
        return jsonify({'message': 'error'}), 401


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
