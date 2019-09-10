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


@app.route('/instances/<zone>/<id>', methods=['GET'])
def get_instance(zone, id):
    user_info = auth.authenticate(request)
    if user_info:
        instance = compute.get_instance(zone, id)

        if instance:
            return render_template(
                'partials/instance.html', instance=instance, zone=zone)
        else:
            return jsonify({'message': 'empty zone'})
    else:
        return jsonify({'message': 'error'}), 401


@app.route('/instances/<zone>', methods=['GET'])
def get_instances(zone):
    user_info = auth.authenticate(request)
    if user_info:
        instances = compute.list_instances(zone)

        if instances:
            return render_template(
                'partials/instances.html', instances=instances, zone=zone)
        else:
            return jsonify({'message': 'empty zone'})
    else:
        return jsonify({'message': 'error'}), 401


@app.route('/instances/<action>', methods=['POST'])
def update_instance(action):
    user_info = auth.authenticate(request)
    if user_info:
        vm = request.form['instance']
        zone = request.form['zone']

        if action == 'start':
            return jsonify(compute.start_vm(zone, vm))
        else:
            return jsonify(compute.stop_vm(zone, vm))

    else:
        return jsonify({'message': 'error'}), 401


@app.route('/operations/<zone>/<operation>', methods=['GET'])
def get_operation(zone, operation):
    user_info = auth.authenticate(request)
    if user_info:
        return jsonify(compute.get_op(zone, operation))
    else:
        return jsonify({'message': 'error'}), 401


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
