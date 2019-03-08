import argparse
import logging
import sys
import yaml

from inspect import getmembers, ismodule, isfunction

import cli
import commands
from modules.trello import Trello


def parse():
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

    for command in getmembers(commands, ismodule):
        func = command[1].main

        if not (isfunction(func)): 
            break

        sub.add_parser(command[0], help=func.__doc__, add_help=False).set_defaults(func=func)

    args, extra_args = parser.parse_known_args()

    # if args.verbose:
        # logging.basicConfig(filename='flask.log',level=logging.DEBUG)
    # else:
        # logging.basicConfig(filename='flask.log',level=logging.INFO)

    with open(args.config, 'r') as t:
        config = roll_up_keys(yaml.load(t))

    return args, extra_args, config

def roll_up_keys(yaml):
    if isinstance(yaml, list):
        for v in yaml:
            roll_up_keys(v)
    elif isinstance(yaml, dict):
        f = {}
        for k,v in yaml.iteritems():
            print(k,v)
            items = k.split(':')
            if(len(items) > 1):
                newv = {':'.join(items[1:]): v}
                f[items[0]] = newv
                yaml[items[0]] = newv
                del yaml[k]
            roll_up_keys(yaml[items[0]])
    return yaml

def main():
    args, extra_args, config = parse()

    try:
        args.func(config, *extra_args)
    except KeyboardInterrupt:
        print('Keyboard interrupt')
        sys.exit(1)
