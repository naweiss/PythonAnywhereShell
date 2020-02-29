import asyncio
import logging

from connection.socket import PythonAnyewhereSocket
from session.remote import PythonAnywhereSession
from terminal.console import PythonAnywhereConsole
from terminal.curses import WindowedTerminal
from terminal.raw import RawTerminal

logger = logging.getLogger(__name__)


async def _open_connection(session_id, console_id, is_windowed=False):
    socket = await PythonAnyewhereSocket.connect(session_id, console_id)

    terminal = WindowedTerminal() if is_windowed else RawTerminal()
    console = PythonAnywhereConsole(terminal, socket)

    tasks = [
        asyncio.ensure_future(console.write_loop()),
        asyncio.ensure_future(console.read_loop()),
        asyncio.ensure_future(console.change_window_size_loop()),
    ]
    try:
        await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        logger.warning('Canceled main loop')


def start_terminal(username, password, is_windowed=False):
    session = PythonAnywhereSession(username=username, password=password)
    session.login()

    consoles = session.list_consoles()
    for index, console in enumerate(consoles):
        print('{}. {}'.format(index, console['name']))

    index = int(input('Please select a console number: '))
    if index < len(consoles):
        loop = asyncio.get_event_loop()
        main_task = asyncio.ensure_future(_open_connection(session_id=session.get_cookie('sessionid'),
                                                           console_id=consoles[index]['id'],
                                                           is_windowed=is_windowed))
        try:
            loop.run_until_complete(main_task)
        except KeyboardInterrupt:
            logging.warning('Ctrl+c pressed')
            main_task.cancel()
        finally:
            loop.run_until_complete(main_task)
