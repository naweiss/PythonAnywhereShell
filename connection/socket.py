import websockets
import logging
import random

logger = logging.getLogger(__name__)


def random_string(length):
    RANDOM_STRING_CHARS = 'abcdefghijklmnopqrstuvwxyz012345'
    return ''.join(random.sample(RANDOM_STRING_CHARS, length))


class PythonAnyewhereSocket(object):
    @staticmethod
    async def connect(session_id, console_id):
        # TODO: find wss URL (e.g. consoles-3/consoles-2) automatically
        logger.info('Opening a new Socket')
        server_id, console_session_id = random.randint(0, 999), random_string(8)
        socket = await websockets.connect('wss://consoles-3.pythonanywhere.com/sj/{}/{}/websocket'.format(server_id, console_session_id))
        wrapper = PythonAnyewhereSocket(socket, session_id, console_id)
        await wrapper.authonticate()
        return wrapper

    def __init__(self, socket, session_id, console_id):
        self.socket = socket
        self.session_id = session_id
        self.console_id = console_id

    async def close(self):
        logger.info('Socket disconnected')
        await self.socket.close()

    async def send(self, data):
        data = '["{}"]'.format(data.replace('"', r'\"'))
        logger.debug('Sending: {}'.format(data))
        try:
            await self.socket.send(data)
        except websockets.exceptions.ConnectionClosedOK:
            pass

    async def recv(self):
        try:
            data = await self.socket.recv()
        except websockets.exceptions.ConnectionClosedOK:
            return
        logger.debug('Received: {}'.format(data))
        prefix, suffix = 'a["', '"]'
        if data.startswith(prefix) and data.endswith(suffix):
            return data[len(prefix): -len(suffix)]

    def is_connected(self):
        return self.socket.open

    async def authonticate(self):
        await self.send(r'\u001b[{};{};;a'.format(self.session_id, self.console_id))

    async def change_window_size(self, width, height):
        await self.send(r'\u001b[8;{};{}t'.format(height, width))
