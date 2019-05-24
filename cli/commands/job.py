import gevent
from gevent.pywsgi import WSGIServer
from flask import Flask
import logging
import sys

import cli
from modules import modules
from engine import Engine


def main(config, *args):
    '''
    run a job from command line
    syntax: run jobname param1=foo param2=bar
    '''

    app = Flask(__name__)
    app.logger.addHandler(logging.StreamHandler(sys.stdout))

    with app.app_context():
        engine = Engine(config, modules, init_triggers=False)
    
    job_name = args[0]
    if not job_name in engine.jobs.keys():
        print('job not found in config: {}'.format(job_name))
        sys.exit(1)

    conditionals = {}

    for arg in args[1:]:
        kv = arg.split('=')
        if not len(kv) == 2:
            print('arg must be key=value, got {}'.format(arg))
            sys.exit(1)
        conditionals[kv[0]] = kv[1]

    engine.jobs[args[0]].run({},conditionals)
