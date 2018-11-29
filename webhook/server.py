import logging
from flask import Flask, request

import cli
from trello import Trello

app = Flask(__name__)

logging.basicConfig(filename='flask.log',level=logging.DEBUG)

@app.route('/', defaults={'path': ''}, methods=['POST', 'GET'])
@app.route('/<path:path>', methods=['POST', 'GET'])
def root(path):
    app.logger.info('{} {} {}'.format(request.method, request.path, request.get_json()))
    return ''
