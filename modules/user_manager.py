import datetime

from google.cloud import datastore

client = datastore.Client()


def is_allowed(user_email):
    query = client.query(kind='AllowedUsers')
    query.add_filter('email', '=', user_email)

    is_allowed = next(iter(query.fetch()), None)

    return is_allowed


def store_visitor(user_info):
    key = client.key('User', user_info['email'])
    user = client.get(key)

    if user is None:
        user = datastore.Entity(key=key)

    user.update(user_info)

    now = datetime.datetime.now()
    user['last_access_time'] = str(now)

    client.put(user)

    return True
