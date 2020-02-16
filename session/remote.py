import logging
import http.client as http_client

from session.utils import LiveSession
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class PythonAnywhereSession(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.connection = LiveSession('https://www.pythonanywhere.com/')

    @staticmethod
    def debug():
        http_client.HTTPConnection.debuglevel = 1

    def login(self):
        logger.info('Logging into pythonanywhere...')
        response = self.connection.get('/login/')
        soup = BeautifulSoup(response.text, features="html.parser")
        csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']

        payload = {
            'auth-username': self.username,
            'auth-password': self.password,
            'csrfmiddlewaretoken': csrf_token,
            'login_view-current_step': 'auth'
        }
        self.connection.post('/login/', data=payload, headers={
            'Referer': 'https://www.pythonanywhere.com/login/',
        })
        logger.info('Logged into pythonanywhere')

    def list_consoles(self):
        response = self.connection.get('/api/v0/user/{}/consoles/'.format(self.username), headers={
            'Referer': 'https://www.pythonanywhere.com/user/{}/consoles/'.format(self.username)
        })
        return response.json()

    def get_cookie(self, cookie_name):
        return self.connection.cookies.get_dict()[cookie_name]
