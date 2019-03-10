import logging
import yaml

from jinja2 import Template

logger = logging.getLogger(__name__)

class Task(object):
    def __init__(self, module, args):
        self.args = args
        self.module = module
        self.name = args.get('name')
        self.loop = args.get('loop')
    
    def get_loop(self, bindings=None):
        logger.debug(self.loop)
        for k, v in self.loop.iteritems():
            if not v or v == '':
                logger.debug({k: []})
                return {k: []}
            if isinstance(v, str) or isinstance(v, unicode):
                loop = {k: Template(v).render(**bindings)}
                logger.debug(loop)
                return loop
        return self.loop

    def run(self, conditionals, bindings=None):
        if bindings == None:
            bindings = conditionals
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
