class Card(object):
    def __init__(self, client, **card):
        self.client = client
        self.id = card['id']
        self.name = card['name']
        self.labels = [client.label(l) for l in card['idLabels']]

    def __repr__(self):
        return '<CARD:{}:{}>'.format(self.id, self.name)
    
    def __eq__(self, other):
        return self.id == other.id

    def add_label(self, label):
        self.client.add_label(self, label)

    def delete_label(self, label):
        self.client.delete_label(self, label)
