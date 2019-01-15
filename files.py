import os
import fnmatch
import hashlib
from .log import get_logger, set_log_file

LOGGER = get_logger(__file__)


def set_log_level_and_file(log_level, log_file=None):
    LOGGER.setLevel(log_level)
    if log_file:
        set_log_file(LOGGER, log_file)


def hash(file, large=False):
    blocksize = 65536
    LOGGER.debug("Hashing file '%s'", file)
    LOGGER.debug("Large file hashing using a blocksize of '%d': '%r'", blocksize, large)
    hasher = hashlib.md5()
    with open(file, 'rb') as hash_file:
        if large:
            buf = hash_file.read(blocksize)
        else:
            buf = hash_file.read()
        if large:
            while len(buf) > 0:
                hasher.update(buf)
                buf = hash_file.read(blocksize)
        else:
            hasher.update(buf)
        hasher.update(buf)
    return hasher.hexdigest()


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
            LOGGER.debug("'%s' matches '%s'", filename, pattern)
            matches.append(os.path.abspath(os.path.join(root, filename)))

        if not recursive:
            break

    LOGGER.debug("Found '%d' files that did match the pattern '%s' in '%s'", len(matches), pattern, start)
    return matches
