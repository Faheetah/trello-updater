from jinja2 import Template

class Task(object):
    def __init__(self, module, args):
        self.args = args
        self.module = module
    
    def run(self, conditionals):
        for task in self.args:
            task_name = self.args[task].keys()[0]
            templated_tasks = {}
            for k, v in self.args[task][task_name].iteritems():
                if isinstance(v, basestring):
                    templated_tasks[k] = Template(v).render(**conditionals)
                else:
                    templated_tasks[k] = v
            print("{0} :: {1}".format(task, templated_tasks))
            self.module.tasks[task_name](**templated_tasks)