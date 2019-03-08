import time

from flask import Blueprint, request, current_app

class GithubWebhook(object):
    def __init__(self, name, module, callback):
        self.name = name
        self.github = module
        self.callback = callback
        self.blueprint = Blueprint(name, __name__)
        self.blueprint.route('/' + name, methods=['HEAD', 'POST'])(self.webhook)
        current_app.register_blueprint(self.blueprint)

    def webhook(self):
        if request.method == 'HEAD':
            return ''
    
        json = request.get_json()
    
        if json:
            # message = u'{} :: {} :: {} :: {}'.format(json['type'], json['id'], json.get('data').get('board', {}).get('name'), json.get('data').get('card', {}).get('name'))
            current_app.logger.info(request.body)
    
        self.callback(json)
    
        return ''
