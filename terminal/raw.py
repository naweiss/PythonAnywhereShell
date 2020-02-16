import sys
import select
import tty
import termios


class RawTerminal(object):
    def __init__(self):
        self.old_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin)

    def close(self):
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)

    @staticmethod
    def read_char():
        read_streams, _, _ = select.select([sys.stdin], [], [], 0)
        if sys.stdin in read_streams:
            return sys.stdin.read(1)

    @staticmethod
    def write_char(char):
        sys.stdout.write(char)
        sys.stdout.flush()
