import logging
from logging import StreamHandler
from os.path import splitext, basename
import sys
import argparse

colors_supported = False
try:
    from colorama import init, Fore, Back, Style
    colors_supported = True
    init()

    class ColorStreamHandler(StreamHandler):
        """ A colorized output SteamHandler """
        colors = {
            'DEBUG': Fore.LIGHTBLUE_EX,
            'INFO': Fore.LIGHTGREEN_EX,
            'WARN': Fore.LIGHTYELLOW_EX,
            'WARNING': Fore.LIGHTYELLOW_EX,
            'ERROR': Fore.LIGHTRED_EX,
            'CRIT': Back.RED + Fore.WHITE,
            'CRITICAL': Back.RED + Fore.WHITE
        }

        def emit(self, record):
            try:
                message = self.format(record)
                self.stream.write(self.colors[record.levelname] + message + Style.RESET_ALL)
                self.stream.write(getattr(self, 'terminator', '\n'))
                self.flush()
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                self.handleError(record)
except ImportError:
    pass


def get_logger(name=None):
    if name:
        logger = logging.getLogger(name)
    else:
        logger = logging.getLogger()

    if not logger.handlers:
        logger.setLevel(logging.INFO)

        if colors_supported:
            console_handler = ColorStreamHandler(sys.stdout)
        else:
            console_handler = StreamHandler(sys.stdout)

        console_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s |%(levelname)-8s| %(message)s', '%Y-%m-%d %H:%M:%S')

        console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)

    return logger


def add_debug_argument(parser):
    parser.add_argument('--debug', action='store_true', required=False, help='Enables debug output')
    return parser
