import logging

from jinja2 import Template

logger = logging.getLogger(__name__)
o
class Task(object):
    def __init__(self, module, args):
        self.args = args
        self.module = module
        self.name = args.get('name')
        self.loop = args.get('loop')
    
    def run(self, conditionals, bindings=None):
        if bindings == None:
            bindings = conditionals
        logger.debug(bindings)
        for task in self.args: 
            task_name = self.args[task].keys()[0] 
            templated_tasks = {}
            for k, v in self.args[task][task_name].iteritems(): 
                if isinstance(v, basestring):
                    templated_tasks[k] = Template(v).render(**bindings)
                else:
                    templated_tasks[k] = v
            print("{0} :: {1}".format(task, templated_tasks))
            return self.module.tasks[task_name](**templated_tasks)
