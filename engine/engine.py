import inspect
import re
import yaml

import logging

from task import Task
from job import Job

logger = logging.getLogger(__name__)

class Engine(object):
    def __init__(self, ruleset, modules):
        self.ruleset = ruleset

        self.executions = {}

        self.modules = {}
        self.init_modules(modules)

        self.jobs = {}
        self.init_jobs()

        self.triggers = {}
        self.init_triggers()

    def init_triggers(self):
        for name, module in self.modules.iteritems():
            for trigger_class in getattr(module, 'triggers', []):
                trigger = trigger_class(name, module, self.callback(name))
                self.triggers[name] = trigger
    
    def init_jobs(self):
        jobs = {j: self.ruleset[j] for j in self.ruleset if j != 'config' and 'triggers' in self.ruleset[j]}
        for job in jobs:
            tasks = [Task(self.modules[t.keys()[0]], t) for t in jobs[job]['tasks']]
            self.jobs[job] = Job(job, jobs[job].get('triggers', {}), tasks)
        

    def init_modules(self, modules):
        for module in modules:
            module_name = module.__name__.lower()
            if module_name not in self.ruleset.get('config', {}):
                initargs = inspect.getargspec(module.__init__)
                # init module if it doesn't have any args aside from self or if it has defaults for all args
                nonselfargs = [a for a in initargs.args if a != 'self']
                if not nonselfargs or (initargs.defaults and len(nonselfargs) == len(initargs.defaults)):
                    self.modules[module_name] = module()
                    logger.debug('loaded module {}'.format(module_name))
        
        # maybe let config be a module and it can handle all of this
        if 'config' in self.ruleset:
            for name in self.ruleset['config']:
                module_config = self.ruleset['config'][name]
                if name in [m.__name__.lower() for m in modules]:
                    module_name = name
                    mc = module_config
                elif len(module_config.keys()) == 1:
                    module_name = module_config.keys()[0]
                    mc = module_config[module_name]
                else:
                    raise Exception('Only one module should be defined')

                module_class = [m for m in modules if m.__name__.lower() == module_name]
                module = module_class[0](**mc)
                self.modules[name] = module
                logger.debug('loaded module {} as {}'.format(self.modules[name].__class__.__name__.lower(), name))
                        
        
    def deep_compare(self, left, right):
        if callable(right):
            return right(left)

        if isinstance(left, str):
            search = re.search(left, right)
            if search:
                return search.string
            return False
        
        if not isinstance(left, dict):
            if left == right:
                return right
            else:
                return False

        if len(left.keys()):
            found = {}
            for key in left.keys():
                if key not in right.keys():
                    return False
                comp = self.deep_compare(left[key], right[key])
                # this isn't good, because we can't compare false triggers, but for now there is no standardization to what a failed trigger is
                # this will at least catch any trigger that explicitly throws False or (most will) not return anything
                # None should probably be the standard though, or we can accept a multiple match like return bool(matched), results in the triggers
                if comp is None or comp is False:
                    return False
                found[key] = comp
            return found
        return True

    def run(self, name, conditionals, bindings=None):
        if bindings == None:
            bindings = {}
        # webhook this is the json
        # something like timer this is the spec with funcs
        bindings.update(conditionals)
        for job in self.jobs:
            for trigger in self.jobs[job].triggers:
                if name in trigger and self.deep_compare(trigger[name], conditionals):
                    bindings.update({"trigger": self.deep_compare(trigger[name], conditionals)})
                    bindings.update(self.executions.get(job, {}))
                    self.executions[job] = self.jobs[job].run(conditionals, bindings)


    def callback(self, name):
        def func(conditionals, bindings=None):
            self.run(name, conditionals, bindings)
        return func
