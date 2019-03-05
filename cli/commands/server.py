import gevent
from gevent.pywsgi import WSGIServer
from flask import Flask

import cli
from modules import modules
from engine import Engine

def main(config, *args):
    'start a webhook server for trello'

    app = Flask(__name__)

    engine = Engine(config, modules)

    for name, webhook in engine.webhooks.iteritems():
        with app.app_context():
            app.register_blueprint(webhook.blueprint)
    
    http_server = WSGIServer(('', 5000), app)
    if not http_server.started:
        http_server.start()

    pid = gevent.os.fork()
    if pid == 0:
        _, _, config = cli.parse()
        for name, webhook in engine.webhooks.iteritems():
            with app.app_context():
                webhook_url = '/'.join((config['config'][name]['webhook'], name))
                app.logger.info('Registering ' + webhook_url)
                webhook.register(webhook_url)

    try:
        http_server._stop_event.wait()
    finally:
        http_server.stop()

