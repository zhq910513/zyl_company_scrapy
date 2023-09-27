from json import loads
from pymongo import MongoClient


class FileStorage(object):

    def __init__(self, settings):
        self.settings = settings

    def get_user_agents(self):
        path = self.settings.get('USER_AGENTS_FILE_PATH')
        with open(path, 'r') as f:
            return loads(f.read())


class MongodbStorage(object):

    def __init__(self, settings):
        self.settings = settings

    def get_user_agents(self):
        uri = self.settings.get('USER_AGENTS_MONGODB_URI')
        db = self.settings.get('USER_AGENTS_DATABASE')
        coll = self.settings.get('USER_AGENTS_COLLECTION')
        client = MongoClient(uri)
        coll = client[db][coll]
        return coll.find(no_cursor_timeout=True)

