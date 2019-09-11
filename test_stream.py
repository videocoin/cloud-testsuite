from utils import pprint
from api import API

api = API('studio.snb', verbose=True)

username = 'dmitry@liveplanet.net'
password = 'new.1ork'

pprint(
    api.user('auth', {
        'email': username,
        'password': password,
    })
)

s = api.stream(
    'create', {
        'name': 'test01',
        'profile_id': 1
    })

pprint(s)

s = api.stream(
    'run', {
        'id': s['id'],
    })

