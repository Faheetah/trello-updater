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
        self.when = args.get('when')
    
    def get_when(self, bindings=None, cond=None):
        # if we are the first run from engine
        if cond is None:
            cond = self.when

        # run through list recursively for multiple conditionals, implied ALL
        if isinstance(cond, list):
            for w in self.when:
                if not self.get_when(bindings=bindings, cond=w):
                    return False
            return True

        # direct string comparison
        if isinstance(cond, str) or isinstance(cond, unicode):
            result = Template(cond).render(**bindings)
            return bool(yaml.safe_load(result))
    
    def get_loop(self, bindings=None):
        for k, v in self.loop.iteritems():
            if not v:
                logger.debug({k: []})
                return {k: []}
            if isinstance(v, str) or isinstance(v, unicode):
                loop = {k: Template(v).render(**bindings)}
                if not loop[k]:
                    logger.debug({k: []})
                    return {k: []}
                logger.debug(loop)
                return loop
        logger.debug(self.loop)
        return self.loop

    def run(self, conditionals, bindings=None):
        if bindings == None:
            bindings = conditionals

        module = [m for m in self.args if m not in ('name', 'when', 'loop')][0]

        if not len(module):
            raise Exception('Task could not be found')

        task_name = self.args[module].keys()[0]

        templated_tasks = {}
        if self.args[module][task_name] is not None:
            for k, v in self.args[module][task_name].iteritems(): 
                if isinstance(v, basestring):
                    templated_tasks[k] = Template(v).render(**bindings)
                else:
                    templated_tasks[k] = v
        logger.info("{0} :: {1}".format(module, templated_tasks))

        if self.name is not None:
            logger.info('Running task {}'.format(self.name))
        else:
            logger.info('Running module {}'.format(task_name))

        return self.module.tasks[task_name](**templated_tasks)
