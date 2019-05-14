import logging

logger = logging.getLogger(__name__)

class Job(object):
    def __init__(self, name, triggers, tasks):
        self.name = name
        self.triggers = triggers
        self.runlist = tasks
        self.tasks = {'run': self.run}

    def run(self, conditionals, bindings):
        executions = {}
        for task in self.runlist:
            bindings.update(executions)
            if task.when and not task.get_when(bindings=bindings):
                if task.name:
                    logger.debug('Skipping {}'.format(task.name))
                else:
                    logger.debug('Skipping anonymous task')
                continue
            # @todo refactor cleaner
            loop = None
            if task.loop:
                loop = task.get_loop(bindings)
                for k, v in loop.iteritems():
                    if isinstance(v, str) or isinstance(v, unicode):
                        loop[k] = yaml.load(v)
            if loop and task.name:
                executions[task.name] = []
                for k, v in loop.iteritems():
                    for i in v:
                        # don't pollute bindings, add each run through the loop to a list in executions
                        local_bindings = bindings.copy()
                        local_bindings.update({k: i})
                        executions[task.name].append(task.run(conditionals, local_bindings))
            elif loop:
                for k, v in loop.iteritems():
                    for i in v:
                        local_bindings = bindings.copy()
                        local_bindings.update({k: i})
                        task.run(conditionals, local_bindings)
            elif task.name:
                executions[task.name] = task.run(conditionals, bindings)
            else:
                task.run(conditionals, bindings)
        return executions
