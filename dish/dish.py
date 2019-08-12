import os

from flask import Flask, request
app = Flask(__name__)
ignore_hosts = os.getenv('DISH_IGNORE_HOSTS', '').lower().split(',')
print('Ignoring hosts:')
for host in ignore_hosts:
    print('>', host)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def dish(path):
    host = request.headers.get('HOST', '').lower()
    report = host not in ignore_hosts
    reported = 'reported' if report else 'not reported'
    return f'Your host is "{host}" ({reported})'
