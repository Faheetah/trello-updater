import logging
import shlex

from subprocess import Popen, PIPE

logger = logging.getLogger(__name__)

class Shell(object):
    def __init__(self, *args, **kwargs):
        self.tasks = {
            'run': self.run
        }

    def run(self, command):
        args = shlex.split(command)

        proc = Popen(args, stdout=PIPE, stderr=PIPE)
        out, err = proc.communicate()
        exitcode = proc.returncode
        logger.info("{} :: {}".format(command, exitcode))
        return {"stdout": out, "stderr": err, "rc": exitcode}
