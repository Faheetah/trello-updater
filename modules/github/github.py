import requests

from webhook import GithubWebhook


class Github(object):
    def __init__(self, repo, secret=None, endpoint=None, *args, **kwargs):
        self.secret = secret
        self.repo = repo

        self.tasks = {}

        self.triggers = [GithubWebhook]
