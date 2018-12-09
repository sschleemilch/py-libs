from os import path, name, environ, remove
import json
from .log import get_logger

LOGGER = get_logger()


class JSONDatabase():
    @staticmethod
    def get_database_path(database_name):
        home = 'USERPROFILE'
        if name != 'nt':
            home = 'HOME'

        database_name = database_name + '.json'
        database_path = path.join(environ[home], database_name)
        return database_path

    def __init__(self, database_name, database_template):
        self.database_path = JSONDatabase.get_database_path(database_name)
        if path.exists(self.database_path):
            LOGGER.debug("Database file '" + self.database_path + "' already exists. Loading content.")
            with open(self.database_path) as f:
                self.data = json.load(f)
        else:
            LOGGER.debug("Database file '" + self.database_path + "' not yet existing. Writing template to file.")
            self.data = database_template
            with open(self.database_path, 'w') as database:
                json.dump(self.data, database)

    def save(self):
        LOGGER.debug("Saving database to disk.")
        with open(self.database_path, 'w') as database:
            json.dump(self.data, database)

    def delete(self):
        LOGGER.warning("Deleting database '" + self.database_path + "'")
        remove(self.database_path)
