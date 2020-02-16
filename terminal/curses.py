import sys
import curses


class WindowedTerminal(object):
    def __init__(self):
        self.stdscr = curses.initscr()
        self.stdscr.nodelay(True)
        curses.noecho()
        curses.cbreak()
        # height, width = stdscr.getmaxyx()

    def close(self):
        self.stdscr.clear()
        curses.echo()
        curses.nocbreak()
        curses.endwin()

    def read_char(self):
        char = self.stdscr.getch()
        if char != curses.ERR:
            return chr(char)

    @staticmethod
    def write_char(char):
        sys.stdout.write(char)
        sys.stdout.flush()
