from flask import Flask, request
app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def dish(path):
    return 'Host: ' + request.headers['HOST']
