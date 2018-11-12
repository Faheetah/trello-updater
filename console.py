import argparse
import sys
import yaml

from inspect import getmembers, ismodule, isfunction

import cli

from trello import Trello

def main():
    parser = argparse.ArgumentParser(
        description='Trello client',
    )

    parser.add_argument('--config', '-c', help='Trello config file', default='trello.yml')
    parser.add_argument('--verbose', '-v', action='store_true', help='show verbose (debug) level output')

    sub = parser.add_subparsers(
        title='commands',
        metavar='COMMAND',
        help='description',
    )

    for command in getmembers(cli, ismodule):
        func = command[1].main

        if not (isfunction(func)): 
            break

        sub.add_parser(command[0], help=func.__doc__, add_help=False).set_defaults(func=func)

    args, extra_args = parser.parse_known_args()

    with open('trello.yml', 'r') as t:
        config = yaml.load(t)
    trello = Trello(config['key'], config['token'], config['board'])

    try:
        args.func(trello, *extra_args)
    except KeyboardInterrupt:
        print('Keyboard interrupt')
        sys.exit(1)

if __name__ == '__main__':
    main()
