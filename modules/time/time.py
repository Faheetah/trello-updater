from threading import Timer

class Time(object):
    def __init__(self, *args, **kwargs):
        print(args, kwargs)
    
    def schedule(delay, callback, *args, **kwargs):

