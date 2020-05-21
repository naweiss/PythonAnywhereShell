import asyncio
import logging

from pythonanywhere_terminal.connection.socket import PythonAnyWhereSocket
from pythonanywhere_terminal.terminal.console import PythonAnywhereConsole
from pythonanywhere_terminal.terminal.curses import WindowedTerminal
from pythonanywhere_terminal.terminal.raw import RawTerminal

logger = logging.getLogger(__name__)


async def _open_connection(session_id, console_id, is_windowed=False):
    socket = await PythonAnyWhereSocket.connect(session_id, console_id)

    terminal = WindowedTerminal() if is_windowed else RawTerminal()
    console = PythonAnywhereConsole(terminal, socket)

    tasks = [
        asyncio.ensure_future(console.write_loop()),
        asyncio.ensure_future(console.read_loop()),
        asyncio.ensure_future(console.change_window_size_loop()),
    ]
    await asyncio.gather(*tasks)


def start_terminal(session_id, console_id, is_windowed=False):
    loop = asyncio.get_event_loop()
    main_task = asyncio.ensure_future(_open_connection(session_id, console_id, is_windowed))
    loop.run_until_complete(main_task)
