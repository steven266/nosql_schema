from abc import ABCMeta, abstractmethod


class AbstractDatabaseHandler():
    """
    Abstract Database Handler
    Abstract class for database handling (e.g. MongoDB).
    Defines basic methods
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def connect(self):
        """
        Connect to a database.
        """
        pass

    @abstractmethod
    def close(self):
        """
        Terminate the connection to the database
        """
        pass

    @abstractmethod
    def drop_collection(self, collection):
        """
        Drops a collection permanently if it exists

        :param collection: The collection's name
        :return: True on success, else False
        """
        pass

    @abstractmethod
    def __getitem__(self, collection):
        """
        Returns the handle to the collection

        :param collection: The collection's name
        :return: Collection handle
        """
        pass

    @abstractmethod
    def __enter__(self):
        """
        Open up a connection
        :return: DatabaseHandler
        """
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_traceback):
        """
        Close connection
        :return: False
        """
        pass

