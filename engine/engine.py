import re

class Engine(object):
    def __init__(self, ruleset, modules):
        self.modules = {}
        self.jobs = {j: ruleset[j] for j in ruleset if j != 'config' and 'triggers' in ruleset[j]}

        if 'config' in ruleset:
            for name in ruleset['config']:
                module_config = ruleset['config'][name]
                if len(module_config.keys()) > 1:
                    raise Exception('Only one module should be defined')
                module_name = module_config.keys()[0]

                module_class = [m for m in modules if m.__name__.lower() == module_name]
                module = module_class[0](self.callback(name), **module_config[module_name])
                self.modules[name] = module
        
        for module in modules:
            self.modules[module.__name__.lower()] = module(self.callback(module.__name__.lower()))

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
            for trigger in self.jobs[job]['triggers']:
                if name in trigger and self.deep_compare(trigger[name], conditionals):
                    for task in self.jobs[job]['tasks']:
                        module_name = task.keys()[0]
                        func_name = task[module_name].keys()[0]
                        func = self.modules[module_name].tasks[func_name]
                        func(**task[module_name][func_name])

    def callback(self, name):
        def func(conditionals):
            self.run(name, conditionals)
        return func
