import re
import yaml

from task import Task
from job import Job

class Engine(object):
    def __init__(self, ruleset, modules):
        if isinstance(ruleset, str):
            self.ruleset = yaml.load(ruleset)
        else:
            self.ruleset = ruleset

        self.executions = {}

        self.modules = {}
        self.init_modules(modules)

        self.jobs = {}
        self.init_jobs()

        self.webhooks = {}
        self.init_webhooks()

    def init_webhooks(self):
        for name, module in self.modules.iteritems():
            for trigger_class in getattr(module, 'triggers', []):
                trigger = trigger_class(name, module, self.callback(name))
                self.webhooks[name] = trigger
    
    def init_jobs(self):
        jobs = {j: self.ruleset[j] for j in self.ruleset if j != 'config' and 'triggers' in self.ruleset[j]}
        for job in jobs:
            tasks = [Task(self.modules[t.keys()[0]], t) for t in jobs[job]['tasks']]
            self.jobs[job] = Job(job, jobs[job].get('triggers', {}), tasks)
        

    def init_modules(self, modules):
        for module in modules:
            if module.__name__.lower() not in self.ruleset.get('config', {}):
                self.modules[module.__name__.lower()] = module()
        
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
                        
        
    def deep_compare(self, left, right):
        if callable(right):
            return right(left)

        if isinstance(left, str):
            return re.search(left, right)
        
        if not isinstance(left, dict):
            return left == right

        for key in left.keys():
            if key not in right.keys():
                return False
            if not self.deep_compare(left[key], right[key]):
                return False
        return True

    def run(self, name, conditionals, bindings=None):
        if bindings == None:
            bindings = {}
        bindings.update(conditionals)
        for job in self.jobs:
            for trigger in self.jobs[job].triggers:
                if name in trigger and self.deep_compare(trigger[name], conditionals):
                    for task in self.jobs[job].tasks:
                        bindings.update(self.executions.get(job, {}))
                        # @todo refactor cleaner
                        loop = task.get_loop(bindings)
                        for k, v in loop.iteritems():
                            if isinstance(v, str) or isinstance(v, unicode):
                                loop[k] = yaml.load(v)
                        if loop and task.name:
                            self.executions[job] = {task.name: []}
                            for k, v in loop.iteritems():
                                for i in v:
                                    # don't pollute bindings, add each run through the loop to a list in executions
                                    local_bindings = bindings.copy()
                                    local_bindings.update({k: i})
                                    self.executions[job][task.name].append(task.run(conditionals, local_bindings))
                        elif loop:
                            for k, v in loop.iteritems():
                                for i in v:
                                    local_bindings = bindings.copy()
                                    local_bindings.update({k: i})
                                    task.run(conditionals, local_bindings)
                        elif task.name:
                            self.executions[job] = {task.name: yaml.dump(task.run(conditionals, bindings))}
                        else:
                            task.run(conditionals, bindings)

    def callback(self, name):
        def func(conditionals, bindings=None):
            self.run(name, conditionals, bindings)
        return func
