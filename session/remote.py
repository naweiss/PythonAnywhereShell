import logging
import os.path
import http.client as http_client

from session.utils import LiveSession
from bs4 import BeautifulSoup
from urllib.parse import urlsplit

logger = logging.getLogger(__name__)


class PythonAnywhereSession(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.connection = LiveSession('https://www.pythonanywhere.com/')

    def __enter__(self):
        self.login()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

    @staticmethod
    def debug():
        http_client.HTTPConnection.debuglevel = 1

    def login(self):
        logger.info('Logging into pythonanywhere...')
        response = self.connection.get('/login/')
        response.raise_for_status()
        soup = BeautifulSoup(response.text, features="html.parser")
        csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']

        payload = {
            'auth-username': self.username,
            'auth-password': self.password,
            'csrfmiddlewaretoken': csrf_token,
            'login_view-current_step': 'auth'
        }
        response = self.connection.post('/login/', data=payload, headers={
            'Referer': 'https://www.pythonanywhere.com/login/',
        })
        response.raise_for_status()
        logger.info('Logged into pythonanywhere')

    def list_consoles(self):
        response = self.connection.get('/api/v0/user/{}/consoles/'.format(self.username))
        response.raise_for_status()
        return response.json()

    def new_console(self, executable):
        response = self.connection.get('/user/{}/consoles/{}/new'.format(self.username, executable), headers={
            'Referer': 'https://www.pythonanywhere.com/user/{}/consoles/'.format(self.username)
        })
        response.raise_for_status()
        return os.path.basename(urlsplit(response.url).path.rstrip(os.path.sep))

    def get_cookie(self, cookie_name):
        return self.connection.cookies.get_dict()[cookie_name]
