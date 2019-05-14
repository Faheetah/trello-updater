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
    
    def start(self, last=None):
        now = datetime.datetime.now()
        threading.Timer(1.0, self.start, kwargs={'last': now}).start()

        if last is not None:
            elapsed = now.second - last.second
            if elapsed < 0:
                elapsed = elapsed + 60
            for second in range(elapsed)[::-1]:
                time = now - datetime.timedelta(seconds=second)
                spec = {
                    "month": time.month,
                    "weekday": time.weekday(),
                    "day": time.day,
                    "hour": time.hour,
                    "minute": time.minute,
                    "second": time.second
                }
                self.callback(spec, bindings={x: getattr(time, x) for x in dir(time)})
    
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
