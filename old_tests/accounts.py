import random
import string
import json
import time
import sys

from api import API
from utils import pprint, rand 

num = 100
emails = ['gen-%s@videocoin.io' % rand() for _ in range(num)]

api = API('studio.dev')

# auth as an admin
api.user('auth', {
    'email': '',
    'password': '',
})

token = api.get_token()

for email in emails:
    api.user('create', {
        'email': email,
        'name': email,
        'password': 'new.1ork',
        'confirm_password': 'new.1ork'
    })

    user = api.user('get', {})
    api.set_token(token)

    while True:
        key = api.accounts('key', {
            'user_id': user['id'],
        })

        key = key.get('key', None)
        if key is None:
            time.sleep(1)
            continue

        key = json.loads(key)

        filename = '{}-{}.json'.format(key.get("address"), email)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(key, f)

        print('{} has been generated for {} user'.format(filename, email))

        break
