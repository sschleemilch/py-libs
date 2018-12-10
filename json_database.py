import os
import json
from .log import get_logger

LOGGER = get_logger(__file__)


def set_log_levels(log_level):
    LOGGER.setLevel(log_level)


class JSONDatabase():
    @staticmethod
    def get_database_path(database_name, database_path='~'):
        database_path = os.path.expanduser(database_path)
        database_name = database_name + '.json'
        database_path = os.path.join(database_path, database_name)
        return database_path

    def __init__(self, database_name, database_template):
        self.database_path = JSONDatabase.get_database_path(database_name)
        if os.path.exists(self.database_path):
            LOGGER.debug("JSON Database file '%s' already exists. Loading content now.", self.database_path)
            with open(self.database_path) as f:
                self.data = json.load(f)
        else:
            LOGGER.debug("JSON Database file '%s' not yet existing. Writing template to file.", self.database_path)
            self.data = database_template
            with open(self.database_path, 'w') as database:
                json.dump(self.data, database)

    def save(self):
        LOGGER.debug("Saving JSON database '%s' to disk.", self.database_path)
        with open(self.database_path, 'w') as database:
            json.dump(self.data, database)

    def delete(self):
        LOGGER.warning("Deleting JSON database '%s'", self.database_path)
        os.remove(self.database_path)