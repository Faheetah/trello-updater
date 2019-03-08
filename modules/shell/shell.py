import logging
import shlex

from subprocess import Popen, PIPE

logger = logging.getLogger(__name__)

class Shell(object):
    def __init__(self, *args, **kwargs):
        self.tasks = {
            'run': self.run
        }

    def run(self, command, chdir=None, env=None, shell=True):
        if not shell:
            command = shlex.split(command)

        proc = Popen(command, stdout=PIPE, stderr=PIPE, cwd=chdir, env=env, shell=shell)
        out, err = proc.communicate()
        exitcode = proc.returncode
        logger.debug("\n{}\n\n{}\n".format(out, err))
        logger.info("{} :: {}".format(command, exitcode))
        return {"stdout": unicode(out.replace('\n', '\\n'), "utf8"), "stderr": unicode(err.replace('\n', '\\n'), "utf8"), "rc": exitcode}
