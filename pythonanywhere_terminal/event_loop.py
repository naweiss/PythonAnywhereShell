import asyncio
import logging

from pythonanywhere_terminal.connection.socket import PythonAnyWhereSocket
from pythonanywhere_terminal.terminal.console import PythonAnywhereConsole
from pythonanywhere_terminal.terminal.curses import WindowedTerminal
from pythonanywhere_terminal.terminal.raw import RawTerminal

logger = logging.getLogger(__name__)


async def _open_connection(session_id, console_id, is_windowed=False, auto_close=False):
    socket = await PythonAnyWhereSocket.connect(session_id, console_id)

    terminal = WindowedTerminal() if is_windowed else RawTerminal()
    console = PythonAnywhereConsole(terminal, socket, auto_close)
    await console.start()


def start_terminal(client, executable, is_windowed=False, auto_close=False):
    console = client.get_console_instance(executable)

    loop = asyncio.get_event_loop()
    main_task = asyncio.ensure_future(_open_connection(session_id=client.get_cookie('sessionid'),
                                                       console_id=console['id'],
                                                       is_windowed=is_windowed,
                                                       auto_close=auto_close))
    loop.run_until_complete(main_task)
