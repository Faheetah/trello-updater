from gevent.pywsgi import WSGIServer

import cli

from trello import Trello
from webhook.server import app

def init_webhook():
    _, _, config = cli.parse()
    trello = Trello(config['key'], config['token'], config['board'])
    webhooks = trello.list_webhooks()

    if not [wh for wh in webhooks if wh['callbackURL'] == config['webhook']]:
        app.logger.info('creating webhook for {}'.format(config['webhook']))
        trello.add_webhook(config['webhook'])


def main(*args):
    'start a webhook server for trello'
    
    http_server = WSGIServer(('', 5000), app)
    if not http_server.started:
        http_server.start()

    init_webhook()

    try:
        http_server._stop_event.wait()
    finally:
        http_server.stop()

