import asyncio
import argparse
import logging

from connection.socket import PythonAnyewhereSocket
from session.remote import PythonAnywhereSession
from terminal.console import PythonAnywhereConsole
from terminal.curses import WindowedTerminal
from terminal.raw import RawTerminal


def init_logger(verbose=False):
    logging_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        filename='pythonanywhere.log',
        filemode='a',
        format='%(asctime)s %(levelname)s: %(message)s',
        datefmt='%H:%M:%S',
        level=logging_level
    )


async def open_terminal(session_id, console_id, is_windowed=False):
    socket = await PythonAnyewhereSocket.connect(session_id, console_id)

    terminal = WindowedTerminal() if is_windowed else RawTerminal()
    console = PythonAnywhereConsole(terminal, socket)
    await asyncio.gather(
        asyncio.ensure_future(console.write_loop()),
        asyncio.ensure_future(console.read_loop()),
        asyncio.ensure_future(console.change_window_size_loop()),
    )


def parse_arguments():
    parser = argparse.ArgumentParser(description='Open a remote console on pythonanywhere account.')
    parser.add_argument('--username', help='account username', required=True)
    parser.add_argument('--password', help='account password', required=True)
    parser.add_argument('--windowed', help='run using curses', action='store_true', default=False)
    parser.add_argument('-v', dest='verbose', help='verbose logging', action='store_true', default=False)

    return parser.parse_args()


def main():
    arguments = parse_arguments()

    init_logger(arguments.verbose)
    session = PythonAnywhereSession(arguments.username, arguments.password)
    session.login()

    consoles = session.list_consoles()
    for index, console in enumerate(consoles):
        print('{}. {}'.format(index, console['name']))

    index = int(input('Please select a console number: '))
    if index < len(consoles):
        loop = asyncio.get_event_loop()
        task = open_terminal(session_id=session.get_cookie('sessionid'),
                             console_id=consoles[index]['id'],
                             is_windowed=arguments.windowed)
        try:
            loop.run_until_complete(task)
        finally:
            task.close()
            loop.stop()


if __name__ == "__main__":
    main()
