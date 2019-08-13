from configparser import ConfigParser
import os
from pathlib import Path

import boto3
from flask import Flask, request


app = Flask(__name__)
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


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def dish(path):
    host = request.headers.get('HOST', '').lower()
    report = host not in ignore_hosts
    reported = 'reported' if report else 'not reported'
    r = sns.publish(TopicArn=sns_id, Message='This is a test', Subject='This is subject')
    print('sns response', r)
    return f'Your host is "{host}" ({reported})'
