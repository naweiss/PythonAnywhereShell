#!/usr/bin/env python3
import configargparse
import logging
import getpass

from pythonanywhere_terminal.event_loop import start_terminal
from pythonanywhere_terminal.session.remote import PythonAnywhereClient, Console

CONFIG_FILES_PATH = ['./.anywhere.ini', '~/.anywhere.ini']


def init_logger(verbose=False):
    logging.basicConfig(
        filename='PythonAnywhere.log',
        filemode='a',
        format='%(asctime)s %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.DEBUG if verbose else logging.INFO
    )


def parse_arguments():
    parser = configargparse.ArgumentParser(description='Open a remote console on PythonAnywhere account.')
    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True

    base_parser = configargparse.ArgumentParser(add_help=False)
    base_parser.add_argument('--username', help='account username', required=True)
    base_parser.add_argument('--password', help='account password')
    base_parser.add_argument('-v', '--verbose', dest='verbose', help='verbose logging',
                             action='store_true', default=False)
    base_parser.add_argument('-c', '--config', is_config_file=True, help='config file path')

    execution_parser = subparsers.add_parser('exec', parents=[base_parser], default_config_files=CONFIG_FILES_PATH)
    execution_parser.add_argument('--windowed', help='run using curses', action='store_true', default=False)
    execution_parser.add_argument('executable', help='open a new console of the give type')

    subparsers.add_parser('list', parents=[base_parser], default_config_files=CONFIG_FILES_PATH)

    return parser.parse_args()


def main():
    arguments = parse_arguments()
    init_logger(verbose=arguments.verbose)

    if not arguments.password:
        arguments.password = getpass.getpass()

    with PythonAnywhereClient(username=arguments.username, password=arguments.password) as client:
        if arguments.command == 'list':
            for console_details in client.list_consoles():
                print(str(Console(console_details)))

        elif arguments.command == 'exec':
            start_terminal(client, arguments.executable)


if __name__ == "__main__":
    main()
