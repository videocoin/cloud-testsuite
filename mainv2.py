import urllib.parse
import requests
import base64
import json
import time
import sys


def pprint(obj):
    print(json.dumps(obj, indent=4))


class API():
    def __init__(self, env):
        self.env = env
        self.api = 'https://%s.videocoin.network' % self.env

    def user(self, action, parameters=[]):
        if action in 'auth':
            resp = self._auth_user(parameters)
            self._set_auth_header(resp.get('token', None))
            return self.auth_header
        elif action in 'settoken':
            self._set_auth_header(parameters.get("token"))
            return self.auth_header
        elif action in 'create':
            resp = self._create_user(parameters)
            self._set_auth_header(resp.get('token', None))
            return resp
        elif action in 'get':
            return self._get_user(parameters)

    def _set_auth_header(self, token):
        self.token = token
        self.auth_header = {'Authorization': 'Bearer %s' % self.token}

    def _auth_user(self, parameters):
        url = '{}/api/v1/auth'.format(self.api)
        parameters = {
            'email': parameters.get('email', None),
            'password': parameters.get('password', None)
        }
        return self._perform_request('post', url, parameters)

    def _get_user(self, parameters):
        url = '{}/api/v1/user'.format(self.api)
        return self._perform_request('get', url, parameters, True)

    def _create_user(self, parameters):
        url = '{}/api/v1/users'.format(self.api)
        return self._perform_request('post', url, parameters)

    def pipelines(self, action, parameters=[]):
        if action in 'list':
            return self._list_pipelines(parameters, '', True)

    def pipeline(self, action, parameters=[]):
        if action in 'get':
            return self._get_pipeline(parameters)
        elif action in 'create':
            return self._create_pipeline(parameters)
        elif action in 'delete':
            return self._delete_pipeline(parameters)
        elif action in 'create-stream':
            return self._create_pipeline_stream(parameters)
        elif action in 'delete-stream':
            return self._delete_pipeline_stream(parameters)
        elif action in 'get-stream':
            return self._get_pipeline_stream(parameters)
        elif action in 'list-streams':
            return self._list_pipeline_streams(parameters)
        elif action in 'run-stream':
            return self._run_pipeline_stream(parameters)
        elif action in 'cancel-stream':
            return self._cancel_pipeline_stream(parameters)

    def _list_pipelines(self, parameters, filter='', auth=False):
        url = '{}/api/v1/pipelines{}?{}'.format(
            self.api, filter, urllib.parse.urlencode(parameters))
        return self._perform_request('get', url, auth=auth)

    def _create_pipeline(self, parameters):
        url = '{}/api/v1/pipelines'.format(self.api)
        return self._perform_request('post', url, parameters, True)

    def _delete_pipeline(self, parameters):
        url = '{}/api/v1/pipelines/{}'.format(
            self.api, parameters.get('pipeline_id'))
        return self._perform_request('delete', url, parameters)

    def _get_pipeline(self, parameters):
        url = '{}/api/v1/pipelines/{}'.format(
            self.api, parameters.get('pipeline_id'))
        return self._perform_request('get', url, None, True)

    def _create_pipeline_stream(self, parameters):
        url = '{}/api/v1/streams'.format(self.api)
        return self._perform_request('post', url, parameters, True)

    def _delete_pipeline_stream(self, parameters):
        url = '{}/api/v1/streams/{}'.format(
            self.api, parameters.get('stream_id'))
        return self._perform_request('delete', url, parameters, True)

    def _get_pipeline_stream(self, parameters):
        url = '{}/api/v1/streams/{}'.format(
            self.api, parameters.get('stream_id'))
        return self._perform_request('get', url, parameters, True)

    def _list_pipeline_streams(self, parameters):
        url = '{}/api/v1/pipelines/{}/streams'.format(
            self.api, parameters.get('pipeline_id'))
        return self._perform_request('get', url, parameters, True)

    def _run_pipeline_stream(self, parameters):
        url = '{}/api/v1/streams/{}/run'.format(
            self.api, parameters.get('stream_id'))
        return self._perform_request('post', url, parameters, True)

    def _cancel_pipeline_stream(self, parameters):
        url = '{}/api/v1/streams/{}/cancel'.format(
            self.api, parameters.get('stream_id'))
        return self._perform_request('post', url, parameters, True)

    def _perform_request(self, method, url, parameters=None, auth=None):
        r = None
        headers = self.auth_header if auth else None
        if method == 'get':
            r = requests.get(url, headers=headers)
        elif method == 'post':
            r = requests.post(url, json=parameters, headers=headers)
        elif method == 'post-form':
            r = requests.post(url, data=parameters, headers=headers)
        elif method == 'put':
            r = requests.put(url, json=parameters, headers=headers)
        elif method == 'put-form':
            r = requests.put(url, data=parameters, headers=headers)
        elif method == 'delete':
            r = requests.delete(url, headers=headers)

        #print(url, r.status_code, headers)
        # print(json.dumps(r.json(), indent=4))
        return r.json()


# thor is dev
# groot is stage
# studio is prod

api = API('studio.dev')

# pprint(
#     api.user('create', {
#         'email': 'kenneth@liveplanet.net',
#         'password': 'new.1ork',
#         'confirm_password': 'new.1ork',
#         'name': 'Kenneth Great'
#     }
#     )
# )

# pprint(
#     api.user('create', {
#         'email': 'kenneth@liveplanet.net',
#         'password': 'new.1ork',
#         'confirm_password': 'new.1ork',
#         'name': 'Kenneth Great'
#     }
#     )
# )

# sys.exit(0)

username = 'dmitry@liveplanet.net'
password = 'new.1ork'

api.user('auth', {
    'email': username,
    'password': password,
})

# pprint(
#     api.user('settoken', {
#         'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1NjAxMzcxOTcsInN1YiI6IjAwOTI5YzA5LTJiOWUtNDRhNi00ZWUyLTg4N2UxZDIwZTFmOCJ9.NSiiDUzO6ASFxLU0u19u3sFQAHq5F8FxmPkA4vJa7x4',
#     })
# )

# pprint(
#     api.user('get', {})
# )

#input("Press enter to continue ...")

p1 = api.pipeline('create', {'name': 'test01', 'profile_id': 1})
# pprint(p1)

pipelines = api.pipelines('list', {}).get('items', None)
pprint(pipelines)
p = pipelines[-1]
pprint(p)

pprint(
    api.pipeline('create-stream', {
        'pipeline_id': p['id']
    })
)

streams = api.pipeline('list-streams', {
    'pipeline_id': p['id']
}).get('items', None)

pprint(streams)
stream = streams[-1]


pprint(
    api.pipeline('run-stream', {
        'stream_id': stream['id']
    })
)

while True:
    time.sleep(3)
    pprint(
        api.pipeline('get-stream', {
            'stream_id': stream['id']
        })
    )

sys.exit(-1)


# pprint(
#     api.pipeline('cancel-stream', {
#         'id': p['id'],
#         'stream_id': j['id']
#     })
# )
