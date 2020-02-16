import asyncio
import logging

from connection.codec import UnicodeCodec

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class PythonAnywhereConsole(object):
    def __init__(self, terminal, socket):
        self.terminal = terminal
        self.socket = socket

    async def read_loop(self):
        try:
            while self.socket.is_connected():
                char = self.terminal.read_char()
                if char is not None:
                    logger.debug('Key down: {}'.format(ord(char)))
                    if char == '\x7f':
                        await self.socket.send(char)
                    else:
                        await self.socket.send(UnicodeCodec.encode(char).replace(r'\x', r'\u00'))
                await asyncio.sleep(0)
        except:
            await self.socket.close()

    async def write_loop(self):
        try:
            while self.socket.is_connected():
                data = await self.socket.recv()
                if len(data) > 0:
                    self.terminal.write_char(UnicodeCodec.decode(data))
                await asyncio.sleep(0)
        except:
            await self.socket.close()
