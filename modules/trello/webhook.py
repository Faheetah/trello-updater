import time

from flask import Blueprint, request, current_app

from modules.timer import Timer

class TrelloWebhook(object):
    def __init__(self, name, module):
        self.name = name
        self.trello = module
        self.blueprint = Blueprint(name, __name__)
        self.blueprint.route('/', methods=['POST'])(self.webhook)

    def register(self, webhook):
        webhooks = self.trello.list_webhooks()
        if not [wh for wh in webhooks if wh['callbackURL'] == webhook]:
            for i in range(5):
                self.app.logger.info('creating webhook for {}'.format(webhook))
                try:
                    self.trello.add_webhook(webhook)
                    return
                except Exception:
                    self.app.logger.info('retrying in {} seconds'.format(i))
                    time.sleep(i)
            self.app.logger.warning('could not create webhook for {}'.format(webhook))


    def webhook(self):
        if request.method == 'HEAD':
            return ''
    
        json = request.get_json().get('action')
    
        if json:
            message = u'{} :: {} :: {} :: {}'.format(json['type'], json['id'], json.get('data').get('board', {}).get('name'), json.get('data').get('card', {}).get('name'))
            current_app.logger.info(message)
    
        return json
    