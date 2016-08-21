from ...db import AbstractCollectionHandler
from ...helper import SchemaId


class CollectionHandler(AbstractCollectionHandler):
    """
    Collection Handler
    Class for collection handling (CRUD methods etc.).
    """
    def __init__(self, collection_handle):
        self.collection_handle = collection_handle

    def find(self, query=None, limit=None, offset=0):
        """
        Find all matching documents in database.

        :param query: Query to match with
        :param limit: Limit of documents to retrieve
        :return: List of documents
        """
        query = CollectionHandler.convert_ids(query)
        return self.collection_handle.find(query, limit)[offset:]

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
    def convert_ids(query, is_id=False):
        """
        Casts all '_id' to 'int'

        :param query: Query that has to be transformed
        :param is_id: Indicates that the current part derived from an '_id'
        :return: Transformed query (dict)
        """
        if not isinstance(query, dict):
            return {}

        new_query = query.copy()

        for k,v in new_query.iteritems():
            if isinstance(v, SchemaId):
                if v.is_list:
                    new_query[k] = [int(id_) for id_ in v.id_list]
                else:
                    new_query[k] = int(v.id_)
            elif k == '_id':
                if isinstance(v, dict):
                    new_query[k] = CollectionHandler.convert_ids(v, True)
                elif type(v) in [str, unicode]:
                    new_query[k] = int(v)
            elif is_id:
                if type(v) in [str, unicode]:
                    new_query[k] = int(v)
                elif type(v) == list:
                    new_query[k] = [int(id_) for id_ in v]
            elif isinstance(v, dict):
                new_query[k] = CollectionHandler.convert_ids(v)

        return new_query
