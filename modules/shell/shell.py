from subprocess import call

class Shell(object):
    def __init__(self, *args, **kwargs):
        self.tasks = {
            'run': self.run
        }

    def run(self, command):
        call(command, shell=True)
