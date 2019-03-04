from threading import Timer
import time


class Timer(object):
    def __init__(self, *args, **kwargs):
        self.tasks = {
            'sleep': self.sleep
        }
    
    def sleep(length):
        time.sleep(length)
