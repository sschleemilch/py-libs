import os
import fnmatch
from log import get_logger

LOGGER = get_logger(__file__)


def set_log_levels(log_level):
    LOGGER.setLevel(log_level)


def get_files_with_pattern(pattern, start='.', recursive=True, skip_hidden_dirs=True, skip_hidden_files=True):
    matches = []
    start = os.path.abspath(start)
    LOGGER.debug("Finding files with pattern '%s' in directory '%s'", pattern, start)
    LOGGER.debug("Recursive: '%r'", recursive)
    LOGGER.debug("Skipping hidden directories: '%r'", skip_hidden_dirs)
    LOGGER.debug("Skipping hidden files: '%r'", skip_hidden_files)
    for root, dirnames, filenames in os.walk(start):
        if skip_hidden_dirs:
            dirnames = [d for d in dirnames if not d[0] == '.']

        if skip_hidden_files:
            filenames = [f for f in filenames if not f[0] == '.']

        for filename in fnmatch.filter(filenames, pattern):
            LOGGER.debug("File '%s' matches pattern criteria '%s'", filename, pattern)
            matches.append(os.path.abspath(os.path.join(root, filename)))

        if not recursive:
            break

    LOGGER.debug("Found '%d' files that did match the pattern '%s' in '%s'", len(matches), pattern, start)
    return matches
