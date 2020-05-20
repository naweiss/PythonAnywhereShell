import sys
import curses


class WindowedTerminal(object):
    def __init__(self):
        self.stdscr = curses.initscr()
        self.stdscr.nodelay(True)
        curses.noecho()
        curses.raw()

    def close(self):
        self.stdscr.clear()
        curses.echo()
        curses.noraw()
        curses.endwin()

    def get_window_size(self):
        h, w = self.stdscr.getmaxyx()
        return w, h

    def read(self):
        char = self.stdscr.getch()
        if char != curses.ERR:
            return chr(char)

    @staticmethod
    def write(text):
        sys.stdout.write(text)
        sys.stdout.flush()
