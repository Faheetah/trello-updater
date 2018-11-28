import logging

from flask import Flask, request

app = Flask(__name__)

logging.basicConfig(filename='flask.log',level=logging.DEBUG)

@app.route('/', defaults={'path': ''}, methods=['POST', 'GET'])
@app.route('/<path:path>', methods=['POST', 'GET'])
def hello_world(path):
    app.logger.info('{} {} {}'.format(request.method, request.path, request.get_json()))
    return ''
