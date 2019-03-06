from jinja2 import Template

class Task(object):
    def __init__(self, module, args):
        self.args = args
        self.module = module
        self.name = args.iteritems().next()[1].pop('name', None)
    
    def run(self, conditionals, bindings=None):
        if bindings == None:
            bindings = conditionals
        for module_name, task in self.args:
            templated_tasks = {}
            for k, v in self.args[task][module_name].iteritems():
                if isinstance(v, basestring):
                    templated_tasks[k] = Template(v).render(**bindings)
                else:
                    templated_tasks[k] = v
            print("{0} :: {1}".format(task, templated_tasks))
            return self.module.tasks[module_name](**templated_tasks)
