def main(trello, card=None):
    'search for a label by name or list all labels on board'
    cards = trello.search()
    
    if card is not None:
        try:
            found = (c for c in cards if c.name == card).next()
            print('{} {}'.format(found.id, found.name))
        except StopIteration:
            print('no cards found')
    else:
        for card in cards:
            print('{} {}'.format(card.id, card.name))
