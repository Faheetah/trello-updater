def main(trello, label_name, search):
    'update labels by label name and search criteria'
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

