from utils import pprint, ffmpeg_rtmp
from api import API
import argparse
import logging
import time
import sys
import os

logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s %(message)s')
logger = logging

def main():
    parser = argparse.ArgumentParser(description='streams')
    parser.add_argument('--env', default='studio.dev')
    parser.add_argument('--username', default=os.environ.get('USERNAME', None))
    parser.add_argument('--password', default=os.environ.get('PASSWORD', None))
    parser.add_argument('--input', default='screen')
    parser.add_argument('--client_id', default=None)
    parser.add_argument('--profile', default='SD')
    parser.add_argument('--file', default=None)
    parser.add_argument('--url', default=None)
    parser.add_argument('--verbose', default=False)

    args = parser.parse_args()
    if not args.username or not args.password:
        exit(parser.print_usage())

    api = API(args.env, verbose=args.verbose)

    username = args.username
    password = args.password

    client_id = args.client_id
    file_path = args.file
    file_url = args.url

    api.user('auth', {
        'email': username,
        'password': password,
    })

    pp = api.profiles('list')['items']
    profile_id = None
    profile = None
    for p in pp:
        if p['name'] == args.profile:
            profile_id = p['id']
            profile = p
            break

    print("Profile ", profile)

    prefix_name = 'rtmp-'
    if file_path or file_url:
        prefix_name = 'file-'

    create_stream_req = {
        'name': prefix_name + 'test-' + str(int(time.time())),
        'profile_id': profile_id
    }

    if file_path or file_url:
        create_stream_req['input_type'] = 'INPUT_TYPE_FILE'

    s = api.stream('create', create_stream_req)

    if client_id:
        m = api.miner('tags', {
            'id': client_id,
            'tags': [
                {"key": "force_task_id", "value": s['id']}
            ]
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

        if s['status'] in ['STREAM_STATUS_CANCELED', 'STREAM_STATUS_PREPARED', 'STREAM_STATUS_FAILED']:
            break

    if s['status'] in ['STREAM_STATUS_CANCELED', 'STREAM_STATUS_FAILED']:
        return

    if file_path is not None:
        api.upload_file(file_path, s['id'])
        api.stream('get', {'id': s['id']})
    elif file_url is not None:
        api.upload_url(file_url, s['id'])
    else:
        logger.debug("stream is ready to consume data: %s", s['rtmp_url'])
        ffmpeg_rtmp(args.input, s['rtmp_url'])

if __name__ == "__main__":
    main()