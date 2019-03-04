import logging
from flask import Blueprint, request, current_app
from pprint import pformat
from . import Trello
from modules.time import Time
from engine.engine import Engine

trello = Blueprint('trello', __name__)


@trello.route('/', methods=['POST', 'GET'])
def webhook():
    if request.method == 'HEAD':
        return ''

    json = request.get_json().get('action')

    if json:
        current_app.logger.debug(pformat(request.get_json()))
        message = u'{} :: {} :: {} :: {}'.format(json['type'], json['id'], json.get('data').get('board', {}).get('name'), json.get('data').get('card', {}).get('name'))
        current_app.logger.info(message)

    with open('trello.yml') as t:
        ruleset = t.read()

    # @todo this needs to get refactored out to spawn multiple apps per trello instance
    e = Engine(ruleset, [Trello, Time])
    e.run('trello', json)
    return ''
