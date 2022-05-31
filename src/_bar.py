from dataclasses import dataclass, field
from datetime import timedelta
from timeit import default_timer as timer

import numpy as np

__all__ = ["Progressbar"]


def _getTerminalSize():
    import os

    env = os.environ

    def ioctl_GWINSZ(fd):
        try:
            import fcntl
            import struct
            import termios

            cr = struct.unpack("hh", fcntl.ioctl(fd, termios.TIOCGWINSZ, "1234"))
        except:
            return
        return cr

    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        cr = (env.get("LINES", 25), env.get("COLUMNS", 80))
    return int(cr[1])


@dataclass
class Progressbar:
    """
    Special method to create custom progress bar

    :param prefix: name of the current bar, default ``'bar: '``
    :type prefix: str, optional
    :param total: number of iteration for the bar
    :type total: int
    """

    iteration: int = field(default_factory=int, init=False)
    total: int = field(default_factory=int, init=True)
    prefix: str = field(default="bar: ", init=True)
    suffix: str = field(default_factory=str, init=False, repr=False)
    decimals: int = field(default=1, init=False)
    length: int = field(default_factory=int, init=False, repr=False)
    fill = "█"
    printEnd = "\r"

    def __post_init__(self):
        try:
            self.length = _getTerminalSize() - len(self.prefix) - 50
        except:
            self.length = 50
        self.start_time = timer()

        self.iteration = 0

        self.suffix = f"{self.iteration} / {self.total}"

        end = timer()
        time_stamp = timedelta(seconds=end - self.start_time)
        remainder = time_stamp / 1 * (self.total - self.iteration)

        percent = f"{np.round(100 * self.iteration / self.total, 3)}"

        _f_length = int(self.length * self.iteration // self.total)
        bar = self.fill * _f_length + "-" * (self.length - _f_length)

        print(
            f"\r{self.prefix} |{bar}| {percent}% {self.suffix} [{str(time_stamp).split('.', maxsplit=1)[0]} - {str(remainder).split('.', maxsplit=1)[0]}]",
            end=self.printEnd,
        )

    def update(self):
        """
        The function is called to move to the next iteration.
        """
        self.iteration += 1

        self.suffix = f"{self.iteration} / {self.total}"

        end = timer()
        time_stamp = timedelta(seconds=end - self.start_time)
        remainder = time_stamp / self.iteration * (self.total - self.iteration)

        percent = f"{np.round(100 * self.iteration / self.total, 1)}"

        _f_length = int(self.length * self.iteration // self.total)
        bar = self.fill * _f_length + "-" * (self.length - _f_length)

        print(
            f"\r{self.prefix} |{bar}| {percent}% {self.suffix} [{str(time_stamp).split('.', maxsplit=1)[0]} - {str(remainder).split('.', maxsplit=1)[0]}]",
            end=self.printEnd,
        )
        # Print New Line on Complete
        if self.iteration == self.total:
            print()
