from ...db import AbstractCollectionHandler
from ...helper import SchemaId


class CollectionHandler(AbstractCollectionHandler):
    """
    Collection Handler
    Class for collection handling (CRUD methods etc.).
    """
    def __init__(self, collection_handle):
        self.collection_handle = collection_handle

    def find(self, query=None, limit=None, offset=0, order_by=None, reverse=False):
        """
        Find all matching documents in database.

        :param query: Query to match with
        :param limit: Limit of documents to retrieve
        :param offset: Offset
        :param order_by: Field to order results by
        :param reverse: Reverse ordering
        :return: List of documents
        """
        query = CollectionHandler.convert_ids(query)
        results = self.collection_handle.find(query, limit)[offset:]

        if order_by is not None:
            def deep_sort(d, order_key):
                keys = order_key.split('.')
                val = d
                for key in keys:
                    val = getattr(val, key)
                    if val is None:
                        return None
                return val

            results = sorted(results, key=lambda d: deep_sort(d, order_by), reverse=reverse)

        return results

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

    def create_index(self, keys, **kwargs):
        """
        Creates an index on collection

        :param keys: list of keys
        :param kwargs: further arguments
        """
        raise NotImplementedError

    def drop_index(self, name):
        """
        Drops an index on collection

        :param name: index name
        """
        raise NotImplementedError

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
            elif isinstance(v, list):
                new_list = [CollectionHandler.convert_ids(x) for x in v]
                new_query[k] = new_list

        return new_query
