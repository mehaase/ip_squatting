from configparser import ConfigParser
import os
from pathlib import Path

import boto3
from flask import Flask, request, Response
from werkzeug.routing import Rule


app = Flask(__name__)
app.url_map.add(Rule('/', endpoint='index'))

here = Path(__file__).parent
config = ConfigParser()
config.read(here / 'conf.ini')
config = config['dish']

sns = boto3.client('sns')
sns_id = config['sns_id']

ignore_hosts = [host.lower().strip() for host in config['ignore_hosts'].split(',')]
print('Dish is ignoring hosts:')
for host in ignore_hosts:
    print(' -', host)


@app.endpoint('index')
def dish():
    host = request.headers.get('HOST', '').lower()
    report = host not in ignore_hosts
    reported = 'REPORTED' if report else 'NOT REPORTED'
    message = f'Connection from {request.remote_addr}\n' \
        f'{request.method} {request.url}\n' \
        f'{request.headers}' \
        f'{request.form}'
    if report:
        r = sns.publish(TopicArn=sns_id, Message=message)
        print('sns response', r)
    return Response(reported + ' ' + message, mimetype='text/plain')
