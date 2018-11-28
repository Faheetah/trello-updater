def main(trello):
    'lists all webhooks for a board'
    
    print(trello.list_webhooks())
