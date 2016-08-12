"""
This module handles the DatabaseHandler assignment
"""


def create_handler(*args, **kwargs):
    """
    Creates an DatabaseHandler instance

    :param database: The name of the database to use, defaults to 'nosqlite'
    :param path: optional database path - for databases: 'nosqlite'
    :param host: optional database host - for databases: 'mongodb'
    :param port: optional database port - for databases: 'mongodb'
    :param name: optional database name - for databases: 'mongodb'
    :return: DatabaseHandler
    """
    database = kwargs.pop('database', 'nosqlite')
    handler = None

    if database == 'nosqlite':
        from .nosqlite import DatabaseHandler
        handler = DatabaseHandler(*args, **kwargs)
    elif database == 'mongodb':
        from .mongodb import DatabaseHandler
        handler = DatabaseHandler(*args, **kwargs)

    return handler


def get_default_handler():
    """
    Get the default DatabaseHandler instance

    :param database: The name of the database to use, defaults to 'nosqlite'
    :param path: optional database path - for databases: 'nosqlite'
    :param host: optional database host - for databases: 'mongodb'
    :param port: optional database port - for databases: 'mongodb'
    :param name: optional database name - for databases: 'mongodb'
    :return: DatabaseHandler
    """
    from .nosqlite import DatabaseHandler
    handler = DatabaseHandler(path=':memory:')
    return handler

