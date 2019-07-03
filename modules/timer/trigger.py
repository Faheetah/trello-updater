import datetime
import logging
import threading
import time


logger = logging.getLogger(__name__)


class TimerTrigger(object):
    def __init__(self, name, module, callback):
        self.name = name
        self.module = module
        self.callback = callback
        t = threading.Thread(target=self.start)
        t.daemon = True
        t.start()
    
    def start(self):
        last = None

        while(True):
            now = datetime.datetime.now()
    
            if last is not None:
                elapsed = now.second - last.second
                if elapsed < 0:
                    elapsed = elapsed + 60
                for second in range(elapsed)[::-1]:
                    current = now - datetime.timedelta(seconds=second)
                    spec = {
                        "month": current.month,
                        "weekday": current.weekday(),
                        "day": current.day,
                        "hour": current.hour,
                        "minute": current.minute,
                        "second": current.second
                    }
                    self.callback(spec, bindings={x: getattr(current, x) for x in dir(current)})
            last = now
    
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                pass
    
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
