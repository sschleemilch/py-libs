import os
from .log import get_logger, set_log_file

LOGGER = get_logger(__file__)


def set_log_level_and_file(log_level, log_file=None):
    LOGGER.setLevel(log_level)
    if log_file:
        set_log_file(LOGGER, log_file)


class inDir:
    def __init__(self, directory):
        if not os.path.exists(directory):
            error_message = "Directory '{}' cannot be found".format(directory)
            LOGGER.error(error_message)
            raise FileNotFoundError(error_message)
        self.target_dir = os.path.abspath(directory)

    def __enter__(self):
        LOGGER.debug("Entering directory '%s'", self.target_dir)
        self.start_dir = os.path.abspath(os.getcwd())
        os.chdir(self.target_dir)

    def __exit__(self, type, value, traceback):
        LOGGER.debug("Leaving directory '%s' and switching back to '%s'", self.target_dir, self.start_dir)
        os.chdir(self.start_dir)
