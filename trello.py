#!/usr/bin/env python

import sys
import yaml

from trello import Trello

def update_labels(label, search):
    with open('trello.yml', 'r') as t:
        config = yaml.load(t)

    trello = Trello(config['key'], config['token'], config['board'])

    try:
        label_id = (l['id'] for l in trello.labels() if l['name'] == label).next()
    except StopIteration:
        print('please create the label {0}'.format(label))
        return
    print('label id found {} {}'.format(label, label_id))

    to_delete_cards = trello.search('label:{0}'.format(label))['cards']
    to_delete = [c['id'] for c in to_delete_cards]
    to_add_cards = trello.search(search)['cards']
    to_add = [c['id'] for c in to_add_cards]

    for card in [c for c in to_delete if c not in to_add]:
        print('deleting {} {} {}'.format(card, label, label_id))
        trello.delete_label(card, label_id)
    
    for card in [c for c in to_add if c not in to_delete]:
        print('adding {} {} {}'.format(card, label, label_id))
        trello.add_label(card, label_id)

def main():
    # i.e. over30 or recent
    label = sys.argv[1]
    # i.e. created:7 or -created:30
    search = sys.argv[2]
    update_labels(label, search)

if __name__ == '__main__':
    main()
