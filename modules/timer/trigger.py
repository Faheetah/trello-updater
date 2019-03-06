import threading
import datetime

class TimerTrigger(object):
    def __init__(self, name, module, callback):
        self.name = name
        self.module = module
        self.callback = callback
        self.start()
    
    def start(self):
        # instead of brute forcing the timer, we can probably
        # use the first start as a seed by parsing all triggers
        # and catching the next one(s)
        # I just want it working for now..
        threading.Timer(1.0, self.start).start()
        now = datetime.datetime.now()

        spec = {
            "month": self.month,
            "weekday": self.weekday,
            "day": self.day,
            "hour": self.hour,
            "minute": self.minute
            "second": self.second
        }

        self.callback(spec)

    def month(self, pattern):
        return pattern == datetime.datetime.now().month

    def weekday(self, pattern):
        return pattern == datetime.datetime.now().weekday()

    def day(self, pattern):
        return pattern == datetime.datetime.now().day

    def hour(self, pattern):
        return pattern == datetime.datetime.now().hour

    def minute(self, pattern):
        return pattern == datetime.datetime.now().minute

    def second(self, pattern):
        return pattern == datetime.datetime.now().second
