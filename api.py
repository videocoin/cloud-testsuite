import urllib.parse
import requests
import curlify
import logging
import base64
import json

logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s %(message)s')
logger = logging

class API():
    def __init__(self, env, verbose=False):
        self.verbose = verbose
        if env == 'local':
            self.api = 'http://localhost:8080'
        else:
            self.env = env
            self.api = 'https://%s.videocoin.network' % self.env

    def user(self, action, parameters=[]):
        if action in 'auth':
            resp = self._auth_user(parameters)
            self._set_auth_header(resp.get('token', None))
            return self.auth_header
        elif action in 'create':
            resp = self._create_user(parameters)
            self._set_auth_header(resp.get('token', None))
            return resp
        elif action in 'get':
            return self._get_user(parameters)
        elif action in 'start_withdraw':
            return self._start_withdraw(parameters)
        elif action in 'end_withdraw':
            return self._withdraw(parameters)

    def set_token(self, token):
        self._set_auth_header(token)
        return self.auth_header

    def get_token(self):
        return self.token

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

    def _start_withdraw(self, parameters):
        url = '{}/api/v1/withdraw/start'.format(self.api)
        return self._perform_request('post', url, parameters, True)

    def _withdraw(self, parameters):
        url = '{}/api/v1/withdraw'.format(self.api)
        return self._perform_request('post', url, parameters, True)

    def accounts(self, action, parameters=[]):
        if action in 'key':
            return self._key(parameters)

    def _key(self, parameters):
        url = '{}/api/v1/user/{}/key'.format(self.api,
                                             parameters.get("user_id"))
        return self._perform_request('get', url, parameters, True)

    def profiles(self, action, parameters=[]):
        if action in 'list':
            return self._list_profiles()

    def _list_profiles(self):
        url = '{}/api/v1/profiles'.format(self.api)
        return self._perform_request('get', url)

    def streams(self, action, parameters=[]):
        if action in 'list':
            return self._list_streams(parameters, '', True)

    def stream(self, action, parameters=[]):
        if action in 'get':
            return self._get_stream(parameters)
        elif action in 'create':
            return self._create_stream(parameters)
        elif action in 'delete':
            return self._delete_stream(parameters)
        elif action in 'run':
            return self._run_stream(parameters)
        elif action in 'stop':
            return self._stop_stream(parameters)

    def _list_streams(self, parameters, filter='', auth=False):
        url = '{}/api/v1/streams{}?{}'.format(
            self.api, filter, urllib.parse.urlencode(parameters))
        return self._perform_request('get', url, auth=auth)

    def _create_stream(self, parameters):
        url = '{}/api/v1/streams'.format(self.api)
        return self._perform_request('post', url, parameters, True)

    def _delete_stream(self, parameters):
        url = '{}/api/v1/streams/{}'.format(
            self.api, parameters.get('id'))
        return self._perform_request('delete', url, parameters)

    def _get_stream(self, parameters):
        url = '{}/api/v1/streams/{}'.format(
            self.api, parameters.get('id'))
        return self._perform_request('get', url, None, True)

    def _create_stream(self, parameters):
        url = '{}/api/v1/streams'.format(self.api)
        return self._perform_request('post', url, parameters, True)

    def _delete_stream(self, parameters):
        url = '{}/api/v1/streams/{}'.format(
            self.api, parameters.get('id'))
        return self._perform_request('delete', url, parameters, True)

    def _run_stream(self, parameters):
        url = '{}/api/v1/streams/{}/run'.format(
            self.api, parameters.get('id'))
        return self._perform_request('post', url, None, True)

    def _stop_stream(self, parameters):
        url = '{}/api/v1/streams/{}/stop'.format(
            self.api, parameters.get('id'))
        return self._perform_request('post', url, None, True)

    def miner(self, action, parameters={}):
        if action in 'create':
            return self._create_miner()
        elif action in 'tags':
            return self._set_miner_tags(parameters)

    def _create_miner(self):
        url = '{}/api/v1/miners'.format(self.api)
        return self._perform_request('post', url, None, True)

    def _set_miner_tags(self, parameters):
        url = '{}/api/v1/miners/{}/tags'.format(
            self.api, parameters.get('id'))
        return self._perform_request('put', url, {"tags": parameters.get('tags')}, True)

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

        if self.verbose:
            logger.debug(curlify.to_curl(r.request))
            logger.debug(url, r.status_code, headers)
            logger.debug(json.dumps(r.json(), indent=4))

        return r.json()
