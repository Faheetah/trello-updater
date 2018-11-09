import requests

class Trello(object):
    def __init__(self, api_key, api_token, board, endpoint=None):
        self.api_key = api_key
        self.api_token = api_token
        self.board = board
        self.endpoint = endpoint or 'https://api.trello.com/1'

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
        return self.request('GET', '/boards/{0}/labels'.format(self.board))
    
    def delete_label(self, card, label):
        return self.request('DELETE', '/cards/{0}/idLabels/{1}'.format(card, label))
    
    def add_label(self, card, label):
        return self.request('POST', '/cards/{0}/idLabels'.format(card), params={'value': label})

    def search(self, query, is_open=True, board=None):
        board = board or self.board
        is_open = 'is:open' if is_open else ''

        params = {
            'query': '{0} board:{1} {2}'.format(query, self.board, is_open),
            'boardId': self.board,
            'cards_limit': 100
        }

        return self.request('GET', '/search', params=params)
