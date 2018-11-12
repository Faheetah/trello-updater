class Label(object):
    def __init__(self, client, **label):
        self.client = client
        self.id = label['id']
        self.name = label['name']

    def __repr__(self):
        return '<LABEL:{}:{}>'.format(self.id, self.name)

    def __eq__(self, other):
        return self.id == other.id
