from abc import ABCMeta, abstractmethod


class AbstractCollectionHandler():
    """
    Abstract Collection Handler
    Abstract class for collection handling (CRUD methods etc.).
    Defines basic methods
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def find(self, query=None, limit=None):
        """
        Find all matching documents in database.

        :param query: Query to match with
        :param limit: Limit of documents to retrieve
        :return: List of documents
        """
        pass

    @abstractmethod
    def delete(self, query):
        """
        Delete one document from database.

        :param query: Query to match with
        :return: True on success, else False
        """
        pass

    @abstractmethod
    def update(self, document):
        """
        Updates the given document in database.

        :param document: Dictionary with _id
        :return: document
        """
        pass

    @abstractmethod
    def insert(self, document):
        """
        Inserts the given document in database.

        :param document: Dictionary
        :return: document
        """
        pass

    @abstractmethod
    def distinct(self, key):
        """
        Get all distinct values for the given key

        :param key: Key to look up
        :return: Set of distinct values
        """
        pass

    @abstractmethod
    def count(self, query=None):
        """
        Count all documents that match the query

        :param query: Query to match with
        :return: Number of documents
        """
        pass
