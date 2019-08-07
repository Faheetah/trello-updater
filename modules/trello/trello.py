import requests

from api.card import Card
from api.label import Label

from webhook import TrelloWebhook

# https://developers.trello.com/reference/#introduction

class Trello(object):
    def __init__(self, api_key, api_token, board, endpoint=None, *args, **kwargs):
        self.api_key = api_key
        self.api_token = api_token
        self.board = board
        self.label_cache = []
        self.member_cache = []
        self.endpoint = endpoint or 'https://api.trello.com/1'

        self.tasks = {
            'addLabel': self.add_label,
            'deleteLabel': self.delete_label,
            'getList': self.get_list,
            'createList': self.create_list,
            'getCard': self.get_card,
            'createCard': self.create_card,
            'updateCard': self.update_card,
            'addAttachment': self.add_attachment,
            'createChecklist': self.create_checklist,
            "search": self.search,
        }

        self.triggers = [TrelloWebhook]

    def request(self, method, uri, *args, **kwargs):
        url = self.endpoint + uri
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

    def members(self):
        if not self.member_cache:
            self.member_cache = self.request('GET', '/boards/{0}/members'.format(self.board))
        return self.member_cache
    
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
    
    def delete_label(self, card, label):
        labels = self.labels()
        l = [l for l in labels if l.name == label][0]
        return self.request('DELETE', '/cards/{0}/idLabels/{1}'.format(card, l.id))

    def add_label(self, card, label):
        labels = self.labels()
        l = [l for l in labels if l.name == label][0]
        return self.request('POST', '/cards/{0}/idLabels'.format(card), params={'value': l.id})

    def add_attachment(self, card, url=None, file=None, name=None, mimeType=None):
        return self.request('POST', '/cards/{0}/attachments'.format(card), params={'url': url, 'file': file, 'name': name, 'mimeType': mimeType})

    def search(self, query, is_open=True, board=None, limit=100):
        if query == None:
            query = ''
        board = board or self.board
        is_open = 'is:open' if is_open else ''

        params = {
            'query': '{0} board:{1} {2}'.format(query, self.board, is_open),
            'boardId': self.board,
            'cards_limit': limit
        }

        req = self.request('GET', '/search', params=params)
        return req
        # we want to eventually revert this but engine can't understand card items yet
        # return [Card(self, **c) for c in req.get('cards')]

    def add_webhook(self, callbackURL, idModel=None):
        if idModel is None:
            idModel = self.get_board()['id']

        return self.request('POST', '/webhooks/?idModel={}&callbackURL={}'.format(idModel, callbackURL))

    # this method is bad, and a misnomer since it can delete more than one webhook
    def delete_webhook(self, webhook):
        webhook_ids = {wh['id'] for wh in self.list_webhooks() if wh['callbackURL'] == webhook['callbackURL']}
        for webhook_id in webhook_ids:
            self.request('DELETE', '/webhooks/{}'.format(webhook_id))
    
    def list_webhooks(self):
        return self.request('GET', '/tokens/{}/webhooks'.format(self.api_token))

    def get_board(self):
        return self.request('GET', '/boards/{}'.format(self.board))

    def list_lists(self):
        return self.request('GET', '/boards/{}/lists'.format(self.board))
    
    def get_list(self, name):
        return [l for l in self.list_lists() if l['name'] == name][0]
    
    def create_list(self, name):
        return self.request('POST', '/boards/{}/lists'.format(self.board), params={'name': name})
    
    def get_card(self, name=None, idCard=None):
        if idCard:
            return self.request('GET', '/cards/{}'.format(idCard))
        if name:
            return [c for c in self.request('GET', '/boards/{}/cards'.format(self.board)) if c['name'] == name][0]
        return False

    def create_card(self, name, description, list, members=None):
        l = self.list_lists()
        if len(l):
            idList = [li for li in l if li['name'] == list][0]['id']
        else:
            idList = self.create_list(list)['id']

        if members is None:
            members = []
        member_ids = [m.get('id') for m in self.members() if m.get('username') in members]

        return self.request('POST', '/cards', params={'idMembers': member_ids,'name': name, 'desc': description, 'idList': idList})

    def create_checklist(self, name, card, checkItems=None):
        checklist = self.request('POST', '/checklists', params={'name': name, 'idCard': card})
        if checkItems:
            for item in checkItems:
                self.request('POST', '/checklists/{}/checkItems/'.format(checklist['id']), params={'name': item})

    # refactor to pass card object, then we can make calls like 
    def update_card(self, card, name=None, pos=None, due=None, idList=None, closed=None, desc=None):
        params = {
            'idList': idList,
            'closed': closed,
            'desc': desc,
            'name': name,
            'pos': pos,
            'due': due
        }
        return self.request('PUT', '/cards/{}'.format(card), params=params)

    def delete_card(self, card):
        return self.request('DELETE', '/cards/{}'.format(card))
