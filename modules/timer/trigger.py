import threading
import datetime

class TimerTrigger(object):
    def __init__(self, name, module, callback):
        self.name = name
        self.module = module
        self.callback = callback
        self.start()
    
    def start(self):
        threading.Timer(10.0, self.start).start()
        now = datetime.datetime.now()
        self.callback({"second": now.second})
