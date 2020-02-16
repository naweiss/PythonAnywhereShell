import asyncio
import argparse
import logging

from connection.socket import PythonAnyewhereSocket
from session.remote import PythonAnywhereSession
from terminal.console import PythonAnywhereConsole
from terminal.curses import WindowedTerminal
from terminal.raw import RawTerminal

logger = logging.getLogger()
logger.addHandler(logging.FileHandler('myapp.log'))
logger.setLevel(logging.INFO)


async def login(session_id, console_id, is_windowed=False):
    logger.info('Connecting to console {}'.format(console_id))
    socket = await PythonAnyewhereSocket.connect(session_id, console_id)

    if is_windowed:
        terminal = WindowedTerminal()
    else:
        terminal = RawTerminal()

    console = PythonAnywhereConsole(terminal, socket)
    try:
        await asyncio.gather(
            asyncio.ensure_future(console.write_loop()),
            asyncio.ensure_future(console.read_loop())
        )
    finally:
        terminal.close()


def parse_arguments():
    parser = argparse.ArgumentParser(description='Open a remote console on pythonanywhere account.')
    parser.add_argument('--username', help='account username', required=True)
    parser.add_argument('--password', help='account password', required=True)
    parser.add_argument('--windowed', action='store_true', default=False)

    return parser.parse_args()


def main():
    arguments = parse_arguments()

    session = PythonAnywhereSession(arguments.username, arguments.password)
    session.login()

    consoles = session.list_consoles()
    for index, console in enumerate(consoles):
        print('{}. {}'.format(index, console['name']))

    index = int(input('Please select a console number: '))
    if index < len(consoles):
        loop = asyncio.get_event_loop()
        task = login(session_id=session.get_cookie('sessionid'),
                     console_id=consoles[index]['id'],
                     is_windowed=arguments.windowed)
        try:
            loop.run_until_complete(task)
        except:
            task.close()


if __name__ == "__main__":
    main()
