import requests

from webhook import ApiWebhook


class Api(object):
    def __init__(self, secret=None, *args, **kwargs):
        self.secret = secret

        self.tasks = {}

        self.global_triggers = [ApiWebhook]

