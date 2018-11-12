def main(trello, label=None):
    'search for a label by name or list all labels on board'
    labels = trello.labels()
    
    if label is not None:
        try:
            found = (l for l in labels if l.name == label).next()
            print('{} {}'.format(found.id, found.name))
        except StopIteration:
            print('no labels found')
    else:
        for label in trello.labels():
            print('{} {}'.format(label.id, label.name))
