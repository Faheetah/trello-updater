import time

from trigger import TimerTrigger

class Timer(object):
    def __init__(self, *args, **kwargs):
        self.tasks = {
            'sleep': self.sleep
        }

        self.triggers = [TimerTrigger]
    
    def sleep(self, length):
        time.sleep(length)
