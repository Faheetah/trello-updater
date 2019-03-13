import time
from datetime import datetime, timedelta

from trigger import TimerTrigger

DAYS = {
    "monday": 1,
    "tuesday": 2,
    "wednesday": 3,
    "thursday": 4,
    "friday": 5,
    "saturday": 6,
    "sunday": 7
}

class Timer(object):
    def __init__(self, *args, **kwargs):
        self.tasks = {
            'weekday': self.weekday,
            'sleep': self.sleep
        }

        self.triggers = [TimerTrigger]
    
    def sleep(self, length):
        time.sleep(length)

    def weekday(self, weekday, time="00:00:00"):
        now = datetime.now()
        tz = datetime.utcnow() - now
        delta = timedelta((7 + DAYS.get(weekday.lower()) - now.weekday()) % 7)
        wd = now + delta + tz
        replace = datetime.strptime(time, "%H:%M:%S")
        return wd.replace(hour=replace.hour, minute=replace.minute, second=replace.second).isoformat()
