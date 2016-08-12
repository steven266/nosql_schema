import nosqlite
from fields import Field
from exceptions import ValidationError

try:
    import config as base_config
except ImportError:
    base_config = None


class Schema:
    @staticmethod
    def get_config():
        """
        Get database configuration

        :return: Configuration dict
        """

        config = dict()

        if base_config:
            config = vars(base_config)

        if 'DATABASE' not in config:
            config['DATABASE'] = 'nosqlite'

        if config['DATABASE'] == 'nosqlite':
            if 'DATABASE_PATH' not in config:
                config['DATABASE_PATH'] = 'database.db'
        elif config['DATABASE'] == 'mongodb':
            if 'DATABASE_HOST' not in config:
                config['DATABASE_HOST'] = 'localhost'

            if 'DATABASE_PORT' not in config:
                config['DATABASE_PORT'] = '27017'

            if 'DATABASE_NAME' not in config:
                config['DATABASE_NAME'] = 'test'

        return config

    @staticmethod
    def get_handle():
        """
        Get database handle

        :return: Database handle
        """
        config = Schema.get_config()
        handle = None

        if config['DATABASE'] == 'nosqlite':
            from nosql_schema.db import nosqlite
            handle = nosqlite.DatabaseHandler(database_path=config['DATABASE_PATH'])
        elif config['DATABASE'] == 'mongodb':
            from nosql_schema.db import mongodb
            handle = mongodb.DatabaseHandler(host=config['DATABASE_HOST'], port=config['DATABASE_PORT'],
                                             database_name=config['DATABASE_NAME'])

        return handle

    def __init__(self, **kwargs):
        self._id = None
        self.__database_handle = Schema.get_handle()

        attributes = self.__class__.__dict__
        # creation by dictionary -> see find / find_one
        try:
            field_dictionary = kwargs.pop('__dictionary')
            if field_dictionary:
                setattr(self, '_id', field_dictionary.pop('_id'))
        except KeyError:
            field_dictionary = None

        # set default values, override with passed values, then with __dictionary
        for k, v in attributes.iteritems():
            if isinstance(v, Field):
                setattr(self, k, v.default)
                if k in kwargs:
                    setattr(self, k, kwargs.pop(k))
                if field_dictionary and k in field_dictionary:
                    setattr(self, k, field_dictionary.pop(k))

    def save(self):
        if not self.__validate():
            return False

        self.__post_process()

        # convert attributes to document
        document = self.__to_dict()

        if self._id is not None:
            # update
            with self.__database_handle as db:
                collection_name = self.__class__.__name__
                collection = db[collection_name]
                collection.update(document)
                return self._id
        else:
            # insert
            with self.__database_handle as db:
                collection_name = self.__class__.__name__
                collection = db[collection_name]
                document = collection.insert(document)
                self._id = document['_id']
                return self._id

    def delete(self):
        document = self.__to_dict()
        if '_id' in document:
            with self.__database_handle as db:
                collection_name = self.__class__.__name__
                collection = db[collection_name]
                return collection.delete({'_id': document['_id']})

    def __validate(self):
        attributes = self.__class__.__dict__
        document = self.__to_dict()
        for k, v in attributes.iteritems():
            if isinstance(v, Field):
                # workaround for getattr(self, k) as it returns class attribute if value is None?!
                value = document.get(k)

                if not v.validate(value=value):
                    raise ValidationError('Invalid value "{0}" for field "{1}"'.format(value, k))

        return True

    def __post_process(self):
        attributes = self.__class__.__dict__
        document = self.__to_dict()
        for k, v in attributes.iteritems():
            if isinstance(v, Field):
                # workaround for getattr(self, k) as it returns class attribute if value is None?!
                value = document.get(k)

                # process value
                value = v.process(value)

                # set attribute to self object
                setattr(self, k, value)

    def __to_dict(self):
        # remove all undefined attributes and add defined attributes
        raw_document = self.__dict__
        document = dict()
        attributes = self.__class__.__dict__

        for k, v in attributes.iteritems():
            if isinstance(v, Field):
                if k in raw_document:
                    document[k] = raw_document[k]
                else:
                    # actually not necessary
                    document[k] = None

        if '_id' in raw_document and raw_document['_id'] is not None:
            document['_id'] = raw_document['_id']

        return document

    # class methods
    @classmethod
    def find(cls, query=None, limit=None, order_by=None, reverse=False):
        database_handle = Schema.get_handle()

        with database_handle as db:
            collection_name = cls.__name__
            collection = db[collection_name]

            results = collection.find(query, limit)
            results = [cls(__dictionary=document) for document in results]

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

    @classmethod
    def find_one(cls, query=None):
        result = cls.find(query, limit=1)
        if len(result) > 0:
            return result[0]
        return None

    @classmethod
    def distinct(cls, key):
        database_handle = Schema.get_handle()
        with database_handle as db:
            collection_name = cls.__name__
            collection = db[collection_name]
            return collection.distinct(key)

    @classmethod
    def count(cls, query=None):
        database_handle = Schema.get_handle()
        with database_handle as db:
            collection_name = cls.__name__
            collection = db[collection_name]

            return collection.count(query)

        return False

    @classmethod
    def drop(cls):
        database_handle = Schema.get_handle()
        with database_handle as db:
            collection_name = cls.__name__
            db.drop_collection(collection_name)

            return True

        return False
