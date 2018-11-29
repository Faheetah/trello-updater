from gevent.pywsgi import WSGIServer

import cli

from trello import Trello
from webhook.server import app

def main(*args):
    'start a webhook server for trello'
    
    _, _, config = cli.parse()
    trello = Trello(config['key'], config['token'], config['board'])
    webhooks = trello.list_webhooks()

    if not [wh for wh in webhooks if wh['callbackURL'] == config['webhook']]:
        app.logger.info('creating webhook for {}'.format(config['webhook']))
        trello.add_webhook(config['webhook'])

    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
