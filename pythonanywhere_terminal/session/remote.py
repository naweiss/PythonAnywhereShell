import logging

from pythonanywhere_terminal.session.utils import CSRFLiveSession

logger = logging.getLogger(__name__)


class Console(object):
    def __init__(self, console_details):
        self.id = console_details['id']
        self.name = console_details['name']
        self.executable = console_details['executable']

    def __str__(self):
        return '{}# {}: running {}'.format(self.id, self.name, self.executable)


class PythonAnywhereClient(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.connection = CSRFLiveSession('https://www.pythonanywhere.com', token_name='csrfmiddlewaretoken')

    def __enter__(self):
        self.login()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

    def login(self):
        logger.info('Logging into pythonanywhere...')
        # Generate CSRF token
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

    def list_consoles(self):
        return self.connection.get('/api/v0/user/{}/consoles/'.format(self.username)).json()

    def new_console(self, executable):
        # Generate CSRF token
        self.connection.get('/')

        payload = {
            'executable': executable,
            'arguments': '',
            'working_directory': None
        }
        response = self.connection.post('/api/v0/user/{}/consoles/'.format(self.username, executable), data=payload, headers={
            'Referer': '{}/user/{}/consoles/'.format(self.connection.prefix_url, self.username)
        })
        return response.json()

    def get_console_instance(self, executable):
        for console in self.list_consoles():
            if console['executable'] == executable:
                return console
        return self.new_console(executable)

    def get_cookie(self, cookie_name):
        return self.connection.cookies.get_dict()[cookie_name]
