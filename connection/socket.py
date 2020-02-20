import websockets
import logging

from websockets.exceptions import ConnectionClosed

logger = logging.getLogger(__name__)


def close_on_error(function):
    async def wrapper(self, *args, **kwargs):
        try:
            return await function(self, *args, **kwargs)
        except ConnectionClosed:
            logger.warning('Error while in {}, closing connection'.format(function.__name__))
            await self.close()

    return wrapper


class PythonAnyewhereSocket(object):
    @staticmethod
    async def connect(session_id, console_id):
        # TODO: find wss URL (e.g. consoles-3/consoles-2) based on console type
        logger.info('Opening a new Socket')
        socket = await websockets.connect('wss://consoles-3.pythonanywhere.com/sj/577/ymljyhge/websocket')
        wrapper = PythonAnyewhereSocket(socket, session_id, console_id)
        await wrapper.authonticate()
        return wrapper

    def __init__(self, socket, session_id, console_id):
        self.socket = socket
        self.session_id = session_id
        self.console_id = console_id
        self.connected = True

    async def close(self):
        if self.connected:
            logger.info('Socket disconnected')
            self.connected = False
            await self.socket.close()

    @close_on_error
    async def send(self, data):
        data = '["{}"]'.format(data)
        logger.debug('Sending: {}'.format(data))
        await self.socket.send(data)

    @close_on_error
    async def recv(self):
        data = await self.socket.recv()
        logger.debug('Received: {}'.format(data))
        prefix, suffix = 'a["', '"]'
        if data.startswith(prefix) and data.endswith(suffix):
            return data[len(prefix): -len(suffix)]

    def is_connected(self):
        return self.connected

    async def authonticate(self):
        await self.send(r'\u001b[{};{};;a'.format(self.session_id, self.console_id))

    async def change_window_size(self, width, height):
        await self.send(r'\u001b[8;{};{}t'.format(height, width))
