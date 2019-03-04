import logging
from flask import Blueprint, request, current_app
from pprint import pformat
from . import Trello
from engine.engine import Engine

trello = Blueprint('trello', __name__)


def init_webhook():
    _, _, config = cli.parse()
    trello = Trello(config['api_key'], config['api_token'], config['board'])
    webhooks = trello.list_webhooks()

    if not [wh for wh in webhooks if wh['callbackURL'] == config['webhook']]:
        for i in range(5):
            current_app.logger.info('creating webhook for {}'.format(config['webhook']))
            try:
                try:
                    trello.delete_webhook(config['webhook'])
                except:
                    pass
                trello.add_webhook(config['webhook'])
                return
            except Exception:
                current_app.logger.info('retrying in {} seconds'.format(i))
                time.sleep(i)
        current_app.logger.warning('could not create webhook for {}'.format(config['webhook']))


@trello.route('/', methods=['POST', 'GET'])
def webhook():
    json = request.get_json().get('action')

    if json:
        current_app.logger.debug(pformat(request.get_json()))
        message = u'{} :: {} :: {} :: {}'.format(json['type'], json['id'], json.get('data').get('board', {}).get('name'), json.get('data').get('card', {}).get('name'))
        current_app.logger.info(message)

    with open('trello.yml') as t:
        ruleset = t.read()

    # @todo this needs to get refactored out to spawn multiple apps per trello instance
    e = Engine(ruleset, [Trello])
    e.callback(json)()
    return ''
