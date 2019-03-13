import time
from datetime import datetime, timedelta

from trigger import TimerTrigger

# Order matters here, matches the datetime weekends
DAYS = [
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday"
]

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
        delta = timedelta((7 + DAYS.index(weekday.lower()) - now.weekday()) % 7)
        wd = now + delta
        replace = datetime.strptime(time, "%H:%M:%S")
        return wd.replace(hour=replace.hour, minute=replace.minute, second=replace.second).isoformat
    