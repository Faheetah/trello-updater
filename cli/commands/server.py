import gevent
from gevent.pywsgi import WSGIServer
from flask import Flask

import cli
from modules import modules
from engine import Engine

def main(*args):
    'start a webhook server for trello'

    app = Flask(__name__)

    with open('trello.yml') as t:
        ruleset = t.read()

    engine = Engine(ruleset, modules)

    for name, webhook in engine.webhooks:
        app.register_blueprint(webhook.blueprint)
    
    http_server = WSGIServer(('', 5000), app)
    if not http_server.started:
        http_server.start()

    pid = gevent.os.fork()
    if pid == 0:
        _, _, config = cli.parse()
        for webhook in engine.webhooks:
            webhook.register()

    try:
        http_server._stop_event.wait()
    finally:
        http_server.stop()

