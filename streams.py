from utils import pprint, ffmpeg_rtmp
from api import API
import argparse
import logging
import time
import os

logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s %(message)s')
logger = logging

def main():
    parser = argparse.ArgumentParser(description='streams')
    parser.add_argument('--env', default='studio.snb')
    parser.add_argument('--username', default=os.environ.get('USERNAME', None))
    parser.add_argument('--password', default=os.environ.get('PASSWORD', None))
    parser.add_argument('--input', default='screen')

    args = parser.parse_args()
    if not args.username or not args.password:
        exit(parser.print_usage())

    api = API(args.env, verbose=False)

    username = args.username
    password = args.password

    api.user('auth', {
        'email': username,
        'password': password,
    })

    pp = api.profiles('list')['items']

    s = api.stream(
        'create', {
            'name': 'test01',
            'profile_id': pp[0]['id']
        })

    s = api.stream(
        'run', {
            'id': s['id'],
        })

    while True:
        time.sleep(3)
        s = api.stream(
            'get', {
                'id': s['id'],
            })

        logger.debug(s)

        if s['status'] in ['STREAM_STATUS_CANCELED', 'STREAM_STATUS_PREPARED', 'STREAM_STATUS_FAILED']:
            break

    logger.info(s)

    if s['status'] in ['STREAM_STATUS_CANCELED', 'STREAM_STATUS_FAILED']:
        logger.error('stream failed')
        return
    print(s['rtmp_url'])
    #ffmpeg_rtmp(args.input, s['rtmp_url'])

if __name__ == "__main__":
    main()