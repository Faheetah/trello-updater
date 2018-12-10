import logging
from flask import Flask, request
from pprint import pformat

from trello.trello import Trello
from engine.engine import Engine

app = Flask(__name__)

@app.route('/', defaults={'path': ''}, methods=['POST', 'GET'])
@app.route('/<path:path>', methods=['POST', 'GET'])
def root(path):
    app.logger.debug(pformat(request.get_json()))

    json = request.get_json()
    message = u'{} :: {} :: {} :: {}'.format(json['type'], json['id'], json.get('data').get('board', {}).get('name'), json.get('data').get('card', {}).get('name'))

    app.logger.info(message)
    with open('trello.yml') as t:
        ruleset = t.read()

    e = Engine(ruleset, [Trello])
    e.callback(json)
    return ''
