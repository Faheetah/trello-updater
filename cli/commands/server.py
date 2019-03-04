import gevent
from gevent.pywsgi import WSGIServer

import cli
import time

from modules.trello import Trello
from modules.trello.server import trello

def init_webhook():
    _, _, config = cli.parse()
    trello = Trello(config['api_key'], config['api_token'], config['board'])
    webhooks = trello.list_webhooks()

    if not [wh for wh in webhooks if wh['callbackURL'] == config['webhook']]:
        for i in range(5):
            trello.logger.info('creating webhook for {}'.format(config['webhook']))
            try:
                trello.add_webhook(config['webhook'])
                return
            except Exception:
                trello.logger.info('retrying in {} seconds'.format(i))
                time.sleep(i)
        trello.logger.warning('could not create webhook for {}'.format(config['webhook']))


def main(*args):
    'start a webhook server for trello'
    
    http_server = WSGIServer(('', 5000), trello)
    if not http_server.started:
        http_server.start()

    pid = gevent.os.fork()
    if pid == 0:
        init_webhook()

    try:
        http_server._stop_event.wait()
    finally:
        http_server.stop()

