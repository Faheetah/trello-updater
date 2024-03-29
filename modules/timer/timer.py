import time
from datetime import datetime, timedelta

from .trigger import TimerTrigger

DAYS = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6
}

class Timer(object):
    def __init__(self, *args, **kwargs):
        self.tasks = {
            'weekday': self.weekday,
            'sleep': self.sleep,
            'now': self.now
        }

        self.triggers = [TimerTrigger]
    
    def sleep(self, length):
        time.sleep(length)

    # diff handling won't be accurate due to utc conversion, especially with dst
    def weekday(self, weekday, time="12:00:00"):
        replace = datetime.strptime(time, "%H:%M:%S")
        now = datetime.now()
        tz = datetime.utcnow() - now
        delta = timedelta((7 + DAYS.get(weekday.lower()) - now.weekday()) % 7)
        wd = now.replace(hour=replace.hour, minute=replace.minute, second=replace.second) + delta + tz
        return wd.isoformat()

    def now(self):
        return datetime.now()
