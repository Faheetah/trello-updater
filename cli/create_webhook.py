def main(trello, callbackURL, idModel=None):
    'create a webhook to a board'
    
    if idModel is None:
        idModel = trello.get_board()['id']

    trello.add_webhook(idModel, callbackURL)
