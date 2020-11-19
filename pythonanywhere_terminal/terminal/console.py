import asyncio
import logging

from pythonanywhere_terminal.async_utils import close_on_error
from pythonanywhere_terminal.connection.codec import UnicodeCodec

logger = logging.getLogger(__name__)


class AbstractConsole(object):
    def __init__(self, terminal, socket):
        self.terminal = terminal
        self.socket = socket
        self.window_size = None

    async def start(self):
        await asyncio.gather(
            asyncio.ensure_future(self.write_loop()),
            asyncio.ensure_future(self.read_loop()),
            asyncio.ensure_future(self.change_window_size_loop())
        )

    async def close(self):
        if self.socket.is_connected():
            await self.socket.close()
        self.terminal.close()

    @close_on_error
    async def change_window_size_loop(self):
        while self.socket.is_connected():
            width, height = self.terminal.get_window_size()
            if (width, height) != self.window_size:
                await self.handle_window_size_change(width, height)
            await asyncio.sleep(0)

    @close_on_error
    async def read_loop(self):
        while self.socket.is_connected():
            char = self.terminal.read()
            if char is not None:
                await self.handle_input(char)
            await asyncio.sleep(0)

    @close_on_error
    async def write_loop(self):
        while self.socket.is_connected():
            raw_data = await self.socket.recv()
            if raw_data is not None:
                await self.handle_output(raw_data)
            await asyncio.sleep(0)

    def handle_window_size_change(self, width, height):
        raise NotImplementedError()

    def handle_output(self, raw_data):
        raise NotImplementedError()

    def handle_input(self, char):
        raise NotImplementedError()


class PythonAnywhereConsole(AbstractConsole):
    CLOSE_PHRASE = '\r\nConsole closed.'
    CTRL_SLASH = '\x1f'

    def __init__(self, terminal, socket, auto_close=False):
        super().__init__(terminal, socket)
        self.auto_close = auto_close

    async def handle_window_size_change(self, width, height):
        await self.socket.change_window_size(width, height)
        self.window_size = (width, height)

    async def handle_output(self, raw_data):
        data = UnicodeCodec.decode(raw_data)

        if self.auto_close and data == self.CLOSE_PHRASE:
            await self.close()
        else:
            self.terminal.write(data)

    async def handle_input(self, data):
        if data == self.CTRL_SLASH:
            await self.close()
        else:
            await self.socket.send(UnicodeCodec.encode(data))
