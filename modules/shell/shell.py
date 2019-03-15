import logging
import shlex

from pprint import pformat
from subprocess import Popen, PIPE

logger = logging.getLogger(__name__)

class Shell(object):
    def __init__(self, env=None, *args, **kwargs):
        self.env = env or {}

        self.tasks = {
            'debug': self.debug,
            'run': self.run
        }

    def debug(self, output):
        if type(output) is str or type(output) is unicode:
            logger.info('debug:\n{}'.format(output))
        else:
            logger.info('debug:\n' + pformat(output))

    def run(self, command, chdir=None, env=None, shell=True):
        if env is None:
            env = {}
        env.update(self.env)

        if not shell:
            command = shlex.split(command)

        proc = Popen(command, stdout=PIPE, stderr=PIPE, cwd=chdir, env=env, shell=shell)
        out, err = proc.communicate()
        exitcode = proc.returncode
        logger.info("{} :: {}".format(command, exitcode))
        if out:
            logger.debug('stdout:\n' + out)
        if err:
            logger.debug('stderr:\n' + err)
        return {"stdout": unicode(out.replace('\n', '\\n'), "utf8"), "stderr": unicode(err.replace('\n', '\\n'), "utf8"), "rc": exitcode}
