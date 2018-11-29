def main(trello, callbackURL, idModel=None):
    'create a webhook to a board'
    
    trello.add_webhook(callbackURL, idModel=idModel)
