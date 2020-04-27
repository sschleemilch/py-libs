import os
import fnmatch
import hashlib
from .log import get_logger

LOGGER = get_logger()


def hash_file(file, large=False):
    if not os.path.exists(file):
        error_message = "File '{}' to hash does not exist".format(file)
        LOGGER.error(error_message)
        raise FileNotFoundError(error_message)

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


def get_files_with_patterns(patterns, start='.', recursive=True, hidden_dirs=False, hidden_files=False, excludes=[]):
    if type(patterns) is not list:
        error_message = "Given pattern is not a list but is '{}'".format(type(patterns))
        LOGGER.error(error_message)
        raise TypeError(error_message)
    files = []
    for pattern in patterns:
        files += get_files_with_pattern(pattern, start, recursive, hidden_dirs, hidden_files, excludes)
    return files


def get_files_with_pattern(pattern, start='.', recursive=True, hidden_dirs=False, hidden_files=False, excludes=[]):
    matches = []
    start = os.path.abspath(start)
    if not os.path.exists(start):
        error_message = "Directory '{}' to start search does not exist".format(start)
        LOGGER.error(error_message)
        raise FileNotFoundError(error_message)
    LOGGER.debug("Finding files with pattern '%s' in directory '%s'", pattern, start)
    LOGGER.debug("Recursive: '%r'", recursive)
    LOGGER.debug("Skipping hidden directories: '%r'", hidden_dirs)
    LOGGER.debug("Skipping hidden files: '%r'", hidden_files)
    for root, dirnames, filenames in os.walk(start):
        if not hidden_dirs:
            dirnames[:] = [d for d in dirnames if not d[0] == '.']
        if not hidden_files:
            filenames[:] = [f for f in filenames if not f[0] == '.']
        filenames[:] = [f for f in filenames if f not in excludes]

        for filename in fnmatch.filter(filenames, pattern):
            LOGGER.debug("'%s' matches '%s'", filename, pattern)
            matches.append(os.path.abspath(os.path.join(root, filename)))

        if not recursive:
            break

    LOGGER.debug("Found '%d' files that did match the pattern '%s' in '%s'", len(matches), pattern, start)
    LOGGER.debug("Found files: '{}'".format(matches))
    return matches
