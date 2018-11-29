import logging
from flask import Flask, request
from pprint import pformat

import cli
from trello import Trello

app = Flask(__name__)

@app.route('/', defaults={'path': ''}, methods=['POST', 'GET'])
@app.route('/<path:path>', methods=['POST', 'GET'])
def root(path):
    app.logger.debug(pformat(request.get_json()))

    json = request.get_json()
    message = '{} :: {} :: {} :: {}'.format(json['action']['type'], json['action']['id'], json['action'].get('data').get('board').get('name'), json['action'].get('data').get('card').get('name'))

    app.logger.info(message)
    return ''
