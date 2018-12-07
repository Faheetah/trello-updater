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
            self.modules[module.__name__.lower()] = module(self.callback(name))
        
    def run(self, name, args, kwargs):
        for job in self.jobs:
            for trigger in self.jobs[job]['triggers']:
                if name in trigger and trigger[name] == kwargs:
                    for task in self.jobs[job]['tasks']:
                        module_name = task.keys()[0]
                        func_name = task[module_name].keys()[0]
                        func = self.modules[module_name].tasks[func_name]
                        kwargs = task[module_name][func_name]
                        func(**kwargs)

    def callback(self, name):
        def func(*args, **kwargs):
            self.run(name, args, kwargs)
        return func
