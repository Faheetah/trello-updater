import requests

from api.card import Card
from api.label import Label

class Trello(object):
    def __init__(self, api_key, api_token, board, endpoint=None, callback=None, *args, **kwargs):
        self.api_key = api_key
        self.api_token = api_token
        self.board = board
        self.label_cache = []
        self.endpoint = endpoint or 'https://api.trello.com/1'
        self.callback = lambda x: callback(x)
        self.tasks = {
            'addLabel': self.add_label,
            'deleteLabel': self.delete_label,
        }

    def request(self, method, uri, *args, **kwargs):
        url = '/'.join((self.endpoint, uri))
        auth = {"key": self.api_key, "token": self.api_token}
        
        if 'params' in kwargs:
            kwargs['params'].update(auth)
        else:
            kwargs['params'] = auth

        req = requests.request(method, url, *args, **kwargs)

        if req.ok:
            return req.json()
        else:
            raise Exception('Could not query API: {0} returned for {1}, {2}'.format(req.status_code, uri, req.text))

    def labels(self):
        if not self.label_cache:
            self.label_cache = self.request('GET', '/boards/{0}/labels'.format(self.board))
        return [Label(self, **l) for l in self.label_cache]
    
    def label(self, label_id):
        if label_id not in [l['id'] for l in self.label_cache]:
            self.labels()
        found = (l for l in self.label_cache if l['id'] == label_id).next()
        if found: 
            return Label(self, **found)
        else:
            raise Exception('Could not find label {} on board'.format(label_id))
    
    # def delete_label(self, card, label):
        # return self.request('DELETE', '/cards/{0}/idLabels/{1}'.format(card.id, label.id))
    
    def delete_label(self, card, label):
        labels = self.labels()
        l = [l for l in labels if l.name == label][0]
        return self.request('DELETE', '/cards/{0}/idLabels/{1}'.format(card, l.id))

    # def add_label(self, card, label):
        # return self.request('POST', '/cards/{0}/idLabels'.format(card.id), params={'value': label.id})

    def add_label(self, card, label):
        labels = self.labels()
        print(card, labels)
        l = [l for l in labels if l.name == label][0]
        return self.request('POST', '/cards/{0}/idLabels'.format(card), params={'value': l.id})

    def search(self, query='', is_open=True, board=None):
        board = board or self.board
        is_open = 'is:open' if is_open else ''

        params = {
            'query': '{0} board:{1} {2}'.format(query, self.board, is_open),
            'boardId': self.board,
            'cards_limit': 100
        }

        req = self.request('GET', '/search', params=params)
        return [Card(self, **c) for c in req.get('cards')]

    def add_webhook(self, callbackURL, idModel=None):
        if idModel is None:
            idModel = self.get_board()['id']

        return self.request('POST', '/webhooks/?idModel={}&callbackURL={}'.format(idModel, callbackURL))

    def delete_webhook(self, webhook):
        return self.request('DELETE', '/webhooks/{}'.format(webhook))
    
    def list_webhooks(self):
        return self.request('GET', '/tokens/{}/webhooks'.format(self.api_token))

    def get_board(self):
        return self.request('GET', '/boards/{}'.format(self.board))
