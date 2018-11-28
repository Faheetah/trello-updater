from gevent.pywsgi import WSGIServer

from webhook.server import app

def main(*args):
    'start a webhook server for trello'
    
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
