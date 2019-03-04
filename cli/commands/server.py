import gevent
from gevent.pywsgi import WSGIServer

import cli
import time

from modules.trello import Trello
from modules.trello.server import trello


app = Flask(__name__)
app.register_blueprint(trello)

def init_webhook():
    _, _, config = cli.parse()
    trello = Trello(config['api_key'], config['api_token'], config['board'])
    webhooks = trello.list_webhooks()

    if not [wh for wh in webhooks if wh['callbackURL'] == config['webhook']]:
        for i in range(5):
            app.logger.info('creating webhook for {}'.format(config['webhook']))
            try:
                trello.add_webhook(config['webhook'])
                return
            except Exception:
                app.logger.info('retrying in {} seconds'.format(i))
                time.sleep(i)
        app.logger.warning('could not create webhook for {}'.format(config['webhook']))


def main(*args):
    'start a webhook server for trello'
    
    http_server = WSGIServer(('', 5000), app)
    if not http_server.started:
        http_server.start()

    pid = gevent.os.fork()
    if pid == 0:
        init_webhook()

    try:
        http_server._stop_event.wait()
    finally:
        http_server.stop()

