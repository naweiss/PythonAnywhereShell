from requests import Session
from urllib.parse import urljoin


class LiveSession(Session):
    def __init__(self, prefix_url=None):
        super(LiveSession, self).__init__()
        self.prefix_url = prefix_url

    def request(self, method, url, *args, **kwargs):
        return super(LiveSession, self).request(method, urljoin(self.prefix_url, url), *args, **kwargs)
