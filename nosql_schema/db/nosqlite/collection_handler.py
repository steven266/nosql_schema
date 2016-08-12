from ...db import AbstractCollectionHandler


class CollectionHandler(AbstractCollectionHandler):
    """
    Collection Handler
    Class for collection handling (CRUD methods etc.).
    """
    def __init__(self, collection_handle):
        self.collection_handle = collection_handle

    def find(self, query=None, limit=None):
        """
        Find all matching documents in database.

        :param query: Query to match with
        :param limit: Limit of documents to retrieve
        :return: List of documents
        """
        query = CollectionHandler.convert_ids(query)
        return self.collection_handle.find(query, limit)

    def delete(self, query):
        """
        Delete one document from database.

        :param query: Query to match with
        :return: True on success, else False
        """
        query = CollectionHandler.convert_ids(query)
        return self.collection_handle.delete(query)

    def update(self, document):
        """
        Updates the given document in database.

        :param document: Dictionary with _id
        :return: document
        """
        document = CollectionHandler.convert_ids(document)
        return self.collection_handle.update(document)

    def insert(self, document):
        """
        Inserts the given document in database.

        :param document: Dictionary
        :return: document
        """
        return self.collection_handle.insert(document)

    def distinct(self, key):
        """
        Get all distinct values for the given key

        :param key: Key to look up
        :return: Set of distinct values
        """
        return self.collection_handle.distinct(key)

    def count(self, query=None):
        """
        Count all documents that match the query

        :param query: Query to match with
        :return: Number of documents
        """
        query = CollectionHandler.convert_ids(query)
        return self.collection_handle.count(query)

    @staticmethod
    def convert_ids(query):
        """
        Casts all '_id' to 'int'

        :param query: Query that has to be transformed
        :return: Transformed query (dict)
        """
        if not isinstance(query, dict):
            return {}

        for k,v in query.iteritems():
            if k == '_id':
                if isinstance(v, dict):
                    query[k] = CollectionHandler.convert_ids(v)
                elif type(v) in [str, unicode]:
                    query[k] = int(v)

        return query
