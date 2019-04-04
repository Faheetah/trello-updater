import time

from flask import Blueprint, request, current_app

class ApiWebhook(object):
    def __init__(self, name, module, callback):
        self.name = name
        self.module = module
        self.callback = callback
        self.blueprint = Blueprint(name, __name__)
        self.blueprint.route('/' + name, methods=['HEAD', 'POST'])(self.webhook)
        current_app.register_blueprint(self.blueprint)

    def webhook(self):
        if request.method == 'HEAD':
            return ''
    
        json = request.get_json()

        if json['secret'] != self.module.secret:
            return 'Auth error'
    
        if json:
            message = u'{}'.format(json['job'])
            current_app.logger.info(message)
    
        self.callback(json)
    
        return ''
