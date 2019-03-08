import gevent
from gevent.pywsgi import WSGIServer
from flask import Flask
import logging
import sys

import cli
from modules import modules
from engine import Engine


def main(config, *args):
    'start a webhook server for trello'

    app = Flask(__name__)
    app.logger.addHandler(logging.StreamHandler(sys.stdout))

    with app.app_context():
        engine = Engine(config, modules)

    http_server = WSGIServer(('', 5000), app)
    if not http_server.started:
        http_server.start()

    pid = gevent.os.fork()
    if pid == 0:
        _, _, config = cli.parse()
        for name, webhook in engine.webhooks.iteritems():
            if getattr(webhook, 'blueprint', None) and getattr(webhook, 'register', None):
                with app.app_context():
                    webhook_url = '/'.join((config['config'][name]['webhook'], name))
                    webhook.register(webhook_url)

    try:
        http_server._stop_event.wait()
    finally:
        http_server.stop()
