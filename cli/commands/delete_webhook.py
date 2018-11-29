def main(trello, webhook):
    'delete a webhook from a board'
    
    trello.delete_webhook(webhook)
