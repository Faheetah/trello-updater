import time


class Timer(object):
    def __init__(self, *args, **kwargs):
        self.tasks = {
            'sleep': self.sleep
        }
    
    def sleep(self, length):
        time.sleep(length)
