from ...db import AbstractDatabaseHandler
from .collection_handler import CollectionHandler
from nosqlite import Connection


class DatabaseHandler(AbstractDatabaseHandler):
    """
    Database Handler
    Handling nosqlite database.
    """

    def __init__(self, path=':memory:'):
        """
        Initialize DatabaseHandler
        :param path: Path to the database or ':memory:'
        """
        self.path = path
        self.connection = None

    def connect(self):
        """
        Connect to a database.
        """
        self.close()
        self.connection = Connection(self.path)

    def close(self):
        """
        Terminate the connection to the database
        """
        if self.connection is not None:
            self.connection.close()

    def drop_collection(self, collection_name):
        """
        Drops a collection permanently if it exists

        :param collection_name: The collection's name
        :return: True on success, else False
        """
        return self.connection.drop_collection(collection_name)

    def __getitem__(self, collection_name):
        """
        Returns the handle to the collection

        :param collection_name: The collection's name
        :return: Collection handle
        """
        collection = None

        if self.connection:
            collection = CollectionHandler(self.connection[collection_name])

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
