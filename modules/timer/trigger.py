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
    
    def parse_date(self, name, pattern, now):
        logger.debug('{} :: {} :: {}'.format(name, pattern, now))
        if isinstance(pattern, int) and pattern == now:
            return now
        if isinstance(pattern, list) and now in pattern:
            return now

    def month(self, pattern):
        now = datetime.datetime.now().month
        return self.parse_date('month', pattern, now)

    def weekday(self, pattern):
        now = datetime.datetime.now().weekday()
        return self.parse_date('weekday', pattern, now)

    def day(self, pattern):
        now = datetime.datetime.now().day
        return self.parse_date('day', pattern, now)

    def hour(self, pattern):
        now = datetime.datetime.now().hour
        return self.parse_date('hour', pattern, now)

    def minute(self, pattern):
        now = datetime.datetime.now().minute
        return self.parse_date('minute', pattern, now)

    def second(self, pattern):
        now = datetime.datetime.now().second
        return self.parse_date('second', pattern, now)
