import threading
import datetime

import logging

logger = logging.getLogger(__name__)

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
            "minute": self.minute,
            "second": self.second
        }

        self.callback(spec)

    def month(self, pattern):
        now = datetime.datetime.now().month
        logger.info('month :: {} :: {}'.format(pattern, now))
        return pattern == now

    def weekday(self, pattern):
        now = datetime.datetime.now().weekday
        logger.info('weekday :: {} :: {}'.format(pattern, now))
        return pattern == now

    def day(self, pattern):
        now = datetime.datetime.now().day
        logger.info('day :: {} :: {}'.format(pattern, now))
        return pattern == now

    def hour(self, pattern):
        now = datetime.datetime.now().hour
        logger.info('hour :: {} :: {}'.format(pattern, now))
        return pattern == now

    def minute(self, pattern):
        now = datetime.datetime.now().minute
        logger.info('minute :: {} :: {}'.format(pattern, now))
        return pattern == now

    def second(self, pattern):
        now = datetime.datetime.now().second
        logger.info('second :: {} :: {}'.format(pattern, now))
        return pattern == now
