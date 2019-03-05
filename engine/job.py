
class Job(object):
    def __init__(self, name, triggers, tasks):
        self.name = name
        self.triggers = triggers
        self.tasks = tasks

    def run(self, payload=None):
        for task in self.tasks:
            task.run()
