import argparse
import logging

from event_loop import start_terminal


def init_logger(verbose=False):
    logging.basicConfig(
        filename='PythonAnywhere.log',
        filemode='a',
        format='%(asctime)s %(levelname)s: %(message)s',
        datefmt='%H:%M:%S',
        level=logging.DEBUG if verbose else logging.INFO
    )


def parse_arguments():
    parser = argparse.ArgumentParser(description='Open a remote console on PythonAnywhere account.')
    parser.add_argument('--username', help='account username', required=True)
    parser.add_argument('--password', help='account password', required=True)
    parser.add_argument('--windowed', help='run using curses', action='store_true', default=False)
    parser.add_argument('-v', dest='verbose', help='verbose logging', action='store_true', default=False)

    return parser.parse_args()


def main():
    arguments = parse_arguments()
    init_logger(verbose=arguments.verbose)
    start_terminal(username=arguments.username, password=arguments.password, is_windowed=arguments.windowed)


if __name__ == "__main__":
    main()
