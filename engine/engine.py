import re
import yaml

class Engine(object):
    def __init__(self, ruleset, modules):
        if isinstance(ruleset, str):
            self.ruleset = yaml.load(ruleset)
        else:
            self.ruleset = ruleset

        self.modules = {}
        self.init_modules(modules)

        self.jobs = {}
        self.init_jobs()
    
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
        if isinstance(left, str):
            return re.search(right, left)

        if not isinstance(left, dict):
            return left == right

        for key in left.keys():
            if key not in right.keys():
                return False
            return self.deep_compare(left[key], right[key])

    def run(self, name, conditionals):
        for job in self.jobs:
            for trigger in self.jobs[job].triggers:
                if name in trigger and self.deep_compare(trigger[name], conditionals):
                    for task in self.jobs[job].tasks:
                        task.run()

    def callback(self, name):
        def func(conditionals):
            self.run(name, conditionals)
        return func

class Job(object):
    def __init__(self, name, triggers, tasks):
        self.name = name
        self.triggers = triggers
        self.tasks = tasks

    def run(self, payload=None):
        for task in self.tasks:
            task.run()

class Task(object):
    def __init__(self, module, args):
        self.args = args
        self.module = module
    
    def run(self):
        for task in self.args:
            task_name = self.args[task].keys()[0]
            self.module.tasks[task_name](**self.args[task][task_name])
