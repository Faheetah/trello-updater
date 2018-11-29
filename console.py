import sys

import cli
from trello import Trello

def main():
    args, extra_args, config = cli.parse()

    trello = Trello(config['key'], config['token'], config['board'])

    try:
        args.func(trello, *extra_args)
    except KeyboardInterrupt:
        print('Keyboard interrupt')
        sys.exit(1)

if __name__ == '__main__':
    main()
