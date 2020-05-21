import logging
import os.path
import http.client as http_client

from pythonanywhere_terminal.session.utils import CSRFLiveSession
from urllib.parse import urlsplit

logger = logging.getLogger(__name__)


class PythonAnywhereClient(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.connection = CSRFLiveSession('https://www.pythonanywhere.com/', token_name='csrfmiddlewaretoken')

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
        self.connection.get('/login/')

        payload = {
            'auth-username': self.username,
            'auth-password': self.password,
            'login_view-current_step': 'auth'
        }
        self.connection.post('/login/', data=payload, headers={
            'Referer': '{}/login/'.format(self.connection.prefix_url),
        })
        logger.info('Logged into pythonanywhere')

    def list_consoles(self, where=None):
        return self.connection.get('/api/v0/user/{}/consoles/'.format(self.username)).json()

    def new_console(self, executable):
        response = self.connection.get('/user/{}/consoles/{}/new'.format(self.username, executable), headers={
            'Referer': '{}/user/{}/consoles/'.format(self.connection.prefix_url, self.username)
        })

        console_url = urlsplit(response.url).path.rstrip(os.path.sep)
        console_id = os.path.basename(console_url)
        if not console_id.isnumeric():
            raise RuntimeError('Failed to create a new console')

        return dict(id=console_id, executable=executable, user=self.username, arguments='', working_directory=None)

    def get_console_instance(self, executable):
        for console in self.list_consoles():
            if console['executable'] == executable:
                return console
        return self.new_console(executable)

    def get_cookie(self, cookie_name):
        return self.connection.cookies.get_dict()[cookie_name]
