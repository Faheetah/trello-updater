#!/usr/bin/env python

import sys
import yaml

from trello import Trello

def update_labels(label_name, search):
    with open('trello.yml', 'r') as t:
        config = yaml.load(t)

    trello = Trello(config['key'], config['token'], config['board'])

    label = (l for l in trello.labels() if l.name == label_name).next()
    print('label id found {} {}'.format(label.id, label.name))

    have_label = trello.search('label:{0}'.format(label_name))
    need_label = trello.search(search)

    for card in [c for c in have_label if c not in need_label]:
        print('deleting {} {}'.format(card, label))
        card.delete_label(label)
    
    for card in [c for c in need_label if c not in have_label]:
        print('adding {} {}'.format(card, label))
        card.add_label(label)

def main():
    # i.e. over30 or recent
    label = sys.argv[1]
    # i.e. created:7 or -created:30
    search = sys.argv[2]
    update_labels(label, search)

if __name__ == '__main__':
    main()
