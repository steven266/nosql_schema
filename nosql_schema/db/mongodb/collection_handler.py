from nosql_schema.db import AbstractCollectionHandler
from bson.objectid import ObjectId


class CollectionHandler(AbstractCollectionHandler):
    """
    Collection Handler
    Class for collection handling (CRUD methods etc.).
    """
    def __init__(self, collection_handle):
        self.collection_handle = collection_handle

    def find(self, query=None, limit=0):
        """
        Find all matching documents in database.

        :param query: Query to match with
        :param limit: Limit of documents to retrieve
        :return: List of documents
        """
        if limit is None:
            limit = 0

        query = CollectionHandler.convert_ids(query)

        result = self.collection_handle.find(filter=query, limit=limit)

        documents = []
        for document in result:
            document['_id'] = str(document['_id'])
            documents.append(document)

        return documents

    def delete(self, query):
        """
        Delete one document from database.

        :param query: Query to match with
        :return: True on success, else False
        """
        query = CollectionHandler.convert_ids(query)

        result = self.collection_handle.delete_one(query)
        if result.deleted_count == 1:
            return True
        return False

    def update(self, document):
        """
        Updates the given document in database.

        :param document: Dictionary with _id
        :return: document
        """
        if '_id' in document:
            doc_id = document['_id']
            del document['_id']
            result = self.collection_handle.replace_one({'_id': ObjectId(doc_id)}, document)
            if result.upserted_id:
                document['_id'] = str(result.upserted_id)
                return document
        return None

    def insert(self, document):
        """
        Inserts the given document in database.

        :param document: Dictionary
        :return: document
        """
        result = self.collection_handle.insert_one(document)
        if result:
            document['_id'] = str(result.inserted_id)
            return document
        return None

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
        Casts all '_id' to 'ObjectId'

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
                    query[k] = ObjectId(unicode(v))

        return query
