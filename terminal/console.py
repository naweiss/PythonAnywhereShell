import asyncio
import logging

from async_utils import close_on_error
from connection.codec import UnicodeCodec

logger = logging.getLogger(__name__)


class PythonAnywhereConsole(object):
    def __init__(self, terminal, socket):
        self.terminal = terminal
        self.socket = socket
        self.window_size = None

    async def close(self):
        self.terminal.close()
        await self.socket.close()

    @close_on_error
    async def change_window_size_loop(self):
        while self.socket.is_connected():
            window_size = self.terminal.get_window_size()
            if window_size != self.window_size:
                width, height = window_size
                await self.socket.change_window_size(width, height)
                self.window_size = window_size
            await asyncio.sleep(0)

    @close_on_error
    async def read_loop(self):
        while self.socket.is_connected():
            char = self.terminal.read_char()
            if char is not None:
                logger.debug('Key down: {}'.format(ord(char)))
                if char == '\x7f':
                    await self.socket.send(char)
                else:
                    await self.socket.send(UnicodeCodec.encode(char).replace(r'\x', r'\u00'))
            await asyncio.sleep(0)

    @close_on_error
    async def write_loop(self):
        while self.socket.is_connected():
            data = await self.socket.recv()
            if data is not None:
                self.terminal.write_char(UnicodeCodec.decode(data))
            await asyncio.sleep(0)
