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
        config = dict()

        if base_config:
            config = vars(base_config)

        if 'DATABASE_PATH' not in config:
            config['DATABASE_PATH'] = 'database.db'

        return config

    def __init__(self, **kwargs):
        self.config = Schema.get_config()
        self._id = None

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
            with nosqlite.Connection(self.config['DATABASE_PATH']) as db:
                collection_name = self.__class__.__name__
                collection = db[collection_name]
                collection.update(document)
                return self._id
        else:
            # insert
            with nosqlite.Connection(self.config['DATABASE_PATH']) as db:
                collection_name = self.__class__.__name__
                collection = db[collection_name]
                document = collection.insert(document)
                self._id = document['_id']
                return self._id

    def delete(self):
        document = self.__to_dict()
        if '_id' in document:
            with nosqlite.Connection(self.config['DATABASE_PATH']) as db:
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
        config = Schema.get_config()
        with nosqlite.Connection(config['DATABASE_PATH']) as db:
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
        # TODO: compose find_one from find with limit 1
        config = Schema.get_config()
        with nosqlite.Connection(config['DATABASE_PATH']) as db:
            collection_name = cls.__name__
            collection = db[collection_name]
            document = collection.find_one(query)

            return cls(__dictionary=document)

    @classmethod
    def distinct(cls, key):
        config = Schema.get_config()
        with nosqlite.Connection(config['DATABASE_PATH']) as db:
            collection_name = cls.__name__
            collection = db[collection_name]
            return collection.distinct(key)

    @classmethod
    def count(cls, query=None):
        config = Schema.get_config()
        with nosqlite.Connection(config['DATABASE_PATH']) as db:
            collection_name = cls.__name__
            collection = db[collection_name]

            return collection.count(query)

        return False

    @classmethod
    def drop(cls):
        config = Schema.get_config()
        with nosqlite.Connection(config['DATABASE_PATH']) as db:
            collection_name = cls.__name__
            db.drop_collection(collection_name)

            return True

        return False
