from ...db import AbstractDatabaseHandler
from .collection_handler import CollectionHandler
from pymongo import MongoClient


class DatabaseHandler(AbstractDatabaseHandler):
    """
    Database Handler
    Handling MongoDB.
    """

    def __init__(self, host='localhost', port='27017', name='test'):
        self.host = host
        self.port = port
        self.database_name = name
        self.client = None

    def connect(self):
        """
        Connect to a database.
        """
        if self.client is None:
            self.client = MongoClient("mongodb://%s:%s" % (self.host, self.port))

    def close(self):
        """
        Terminate the connection to the database
        """
        # Garbage collection will handle it
        del self.client
        self.client = None

    def drop_collection(self, collection_name):
        """
        Drops a collection permanently if it exists

        :param collection_name: The collection's name
        :return: True on success, else False
        """
        if self.client:
            return self.client.drop_collection(collection_name)
        return False

    def __getitem__(self, collection_name):
        """
        Returns the handle to the collection

        :param collection_name: The collection's name
        :return: Collection handle
        """
        collection = None

        if self.client:
            collection = CollectionHandler(self.client[self.database_name][collection_name])

        return collection

    def __enter__(self):
        """
        Open up a connection
        :return: DatabaseHandler
        """
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_traceback):
        """
        Close connection
        :return: False
        """
        self.close()
        return False
