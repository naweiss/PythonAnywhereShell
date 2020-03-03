import os
import sys
import select
import tty
import termios
import fcntl
import struct


class RawTerminal(object):
    def __init__(self):
        self.old_settings = termios.tcgetattr(sys.stdin)
        tty.setraw(sys.stdin)

    def close(self):
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)

    @staticmethod
    def get_window_size():
        h, w, hp, wp = struct.unpack('HHHH', fcntl.ioctl(0, termios.TIOCGWINSZ, struct.pack('HHHH', 0, 0, 0, 0)))
        return w, h

    @staticmethod
    def read():
        read_streams, _, _ = select.select([sys.stdin], [], [], 0)
        if sys.stdin in read_streams:
            return os.read(sys.stdin.fileno(), 4096).decode('utf-8')

    @staticmethod
    def write(text):
        sys.stdout.write(text)
        sys.stdout.flush()
