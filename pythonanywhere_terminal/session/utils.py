from requests import Session
from urllib.parse import urljoin
from bs4 import BeautifulSoup


class ValidSession(Session):
    def request(self, method, url, *args, **kwargs):
        response = super(ValidSession, self).request(method, url, *args, **kwargs)
        response.raise_for_status()
        return response


class LiveSession(ValidSession):
    def __init__(self, prefix_url=None):
        super(LiveSession, self).__init__()
        self.prefix_url = prefix_url

    def request(self, method, url, *args, **kwargs):
        return super(LiveSession, self).request(method, urljoin(self.prefix_url, url), *args, **kwargs)


class CSRFLiveSession(LiveSession):
    def __init__(self, prefix_url=None, token_name=None):
        super(CSRFLiveSession, self).__init__(prefix_url)
        self.token_name = token_name
        self.token_value = ''

    def post(self, url, data=None, json=None, **kwargs):
        if data is None:
            data = {}

        data.update({self.token_name: self.token_value})
        return super(CSRFLiveSession, self).post(url, data, json, **kwargs)

    def _get_token(self, text):
        soup = BeautifulSoup(text, features="html.parser")
        elements = soup.find_all('input', {'name': self.token_name})
        if len(elements):
            return elements[0]['value']

    def get(self, url, **kwargs):
        response = super(CSRFLiveSession, self).get(url, **kwargs)
        if response.ok:
            self.token_value = self._get_token(response.text)
        return response
