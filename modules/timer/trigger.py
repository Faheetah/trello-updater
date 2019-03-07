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

        # this isn't going to be 100% accurate because it's not straightforward
        # to generate time right, will cause possible off by 1 but for now shouldn't be
        # too impacting
        self.callback(spec, bindings={x: getattr(now, x) for x in dir(now)})

    def month(self, pattern):
        now = datetime.datetime.now().month
        logger.info('month :: {} :: {}'.format(pattern, now))
        if isinstance(pattern, str):
            return pattern == now
        if isinstance(pattern, list):
            return now in pattern

    def weekday(self, pattern):
        now = datetime.datetime.now().weekday()
        logger.info('weekday :: {} :: {}'.format(pattern, now))
        if isinstance(pattern, list):
            return now in pattern
        else:
            return now == pattern

    def day(self, pattern):
        now = datetime.datetime.now().day
        logger.info('day :: {} :: {}'.format(pattern, now))
        if isinstance(pattern, list):
            return now in pattern
        else:
            return now == pattern

    def hour(self, pattern):
        now = datetime.datetime.now().hour
        logger.info('hour :: {} :: {}'.format(pattern, now))
        if isinstance(pattern, list):
            return now in pattern
        else:
            return now == pattern

    def minute(self, pattern):
        now = datetime.datetime.now().minute
        logger.info('minute :: {} :: {}'.format(pattern, now))
        if isinstance(pattern, list):
            return now in pattern
        else:
            return now == pattern

    def second(self, pattern):
        now = datetime.datetime.now().second
        logger.debug('second :: {} :: {}'.format(pattern, now))
        if isinstance(pattern, list):
            return now in pattern
        else:
            return now == pattern
