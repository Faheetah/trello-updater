# Trello Updater

So far all this does is synchchronize open cards with the given label name, i.e.:

```
./trello.py "recent" "created:7"
```

This will find all open cards created in the past 7 days and label them with the "recent" label, and delete any cards with the "recent" label that did not match the search. The search argument matches the search in Trello and implicitly uses "is:open board:YOURBOARD".

# Config

Config is formatted yaml

```
key: YOUR_API_KEY
token: YOUR_API_TOKEN
board: YOUR_BOARD
```

# Future plans

Better search criteria, more CRUD options, option to specify rules to keep cards synchronized.

In the far future, possibility to keep cards synchronized however this would rely on local state and a daemon to track when a given card needs updating and a webhook for when a card gets added.

If functionality gets complete enough, possibly will update to be a powerup too.
