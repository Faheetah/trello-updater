import argparse
import logging
import os
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

    parser.add_argument('--config', '-c', help='Trello config file', default=os.environ.get('TRELLO_CONFIG', 'trello.yml'))
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

    config = parse_config_path(args.config)

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)


    return args, extra_args, config

def parse_config_path(path):
    config = {}

    if os.path.isfile(path):    
        with open(path, 'r') as t:
            config = yaml.load(t)

    if os.path.isdir(path):
        for job in os.listdir(path):
            job_path = os.path.join(path, job)
            job_name = os.path.splitext(job)[0]

            if os.path.isfile(job_path):
                if job_name in config:
                    print('duplicate key {}'.format(job))
                    sys.exit(1)
                with open(job_path, 'r') as t:
                    config[job_name] = yaml.load(t)
            
            # this could be refactored cleaner
            if os.path.isdir(job_path):
                config[job_name] = {}
                for task in os.listdir(job_path):
                    task_path = os.path.join(job_path, task)
                    task_name = os.path.splitext(task)[0]

                    if os.path.isfile(task_path):
                        if task_name in config[job_name]:
                            print('duplicate key {}'.format(job))
                            sys.exit(1)
                        with open(task_path, 'r') as t:
                            config[job_name][task_name] = yaml.load(t)


    return roll_up_keys(config)

def roll_up_keys(yaml):
    if isinstance(yaml, list):
        for v in yaml:
            roll_up_keys(v)
    elif isinstance(yaml, dict):
        f = {}
        for k,v in yaml.iteritems():
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
