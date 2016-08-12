nosql_schema
===========

``nosql_schema`` is a simple object document mapper for NoSQL databases like
[nosqlite](https://github.com/shaunduncan/nosqlite) or [MongoDB](https://www.mongodb.com/).
 
It provides a basic Schema-class that let's you define simple classes that are mapped to NoSQL collections.
nosql_schema provides simple validators for a minimal amount of field-types.
 
Example:

```python
import os
from nosql_schema import Schema
from nosql_schema.fields import StringField, EmailField, DictField, ListField
 
Schema.__config__ = {
    'database'  : 'nosqlite',
    'path'      : os.path.dirname(__file__) + '/database.db'
}
 
class Publication(Schema):
    title = StringField()
    content = StringField()
    author = DictField(allowed_fields={
        'name': StringField(),
        'email': EmailField(),
    })
    keywords = ListField()
    
publication = Publication()
publication.title = 'My First Publication'
publication.author = {
    'name': 'John Doe',
    'email': 'john.doe@example.org'
}
publication.keywords = ['scientific', 'neuro-sciences']
publication.save()

print Publication.find()
```

To configure **MongoDB**, set the following *before* using nosql_schema:

```python
from nosql_schema import Schema

Schema.__config__ = {
    'database': 'mongodb',
    'host': 'localhost',
    'port': '27017',
    'name': 'your-database-name'
}
```

Further Requirements
------------------------
For **nosqlite** you will need the `nosqlite` python package.
For **MongoDB** you will need the `pymongo` python package.


Contribution and License
------------------------
Developed by Steven Cardoso <hello@steven266.de> and is licensed under the
terms of a MIT license.

Contributions are welcomed and appreciated. Writing (new) test-cases is
appreciated.
