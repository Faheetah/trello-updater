import time

from flask import Blueprint, request, current_app

class TrelloWebhook(object):
    def __init__(self, name, module, callback):
        self.name = name
        self.trello = module
        self.callback = callback
        self.blueprint = Blueprint(name, __name__)
        self.blueprint.route('/' + name, methods=['HEAD', 'POST'])(self.webhook)
        current_app.register_blueprint(self.blueprint)

    def register(self, webhook):
        webhooks = self.trello.list_webhooks()
        current_app.logger.info(webhooks)
        if not [wh for wh in webhooks if wh['callbackURL'] == webhook and wh['idModel'] != self.trello.get_board(self.trello.board)['idModel']]:
            for i in range(5):
                current_app.logger.info('creating webhook for {}'.format(webhook))
                try:
                    self.trello.add_webhook(webhook)
                    return
                except Exception:
                    current_app.logger.info('retrying in {} seconds'.format(i))
                    time.sleep(i)
            current_app.logger.warning('could not create webhook for {}'.format(webhook))


    def webhook(self):
        if request.method == 'HEAD':
            return ''
    
        json = request.get_json().get('action')
    
        if json:
            message = u'{} :: {} :: {} :: {}'.format(json['type'], json['id'], json.get('data').get('board', {}).get('name'), json.get('data').get('card', {}).get('name'))
            current_app.logger.info(message)
    
        self.callback(json)
    
        return ''
