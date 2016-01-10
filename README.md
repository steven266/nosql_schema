nosql_schema
===========

``nosqlite_schema`` is a simple object document mapper for [nosqlite](https://github.com/shaunduncan/nosqlite).
It provides a basic Schema-class that let's you define simple classes that are mapped to nosqlite documents.
nosql_schema provides simple validators for a minimal amount of field-types. Example::

```python
from nosql_schema.schema import Schema
from nosql_schema.fields import StringField, EmailField, DictField, ListField


class Publication(Schema):
    title = StringField()
    content = StringField()
    author = DictField(allowed_fields={
        'name': StringField(),
        'email': EmailField(),
    })
    keywords = ListField()
```


Contribution and License
------------------------
Developed by Steven Cardoso <hello@steven266.de> and is licensed under the
terms of a MIT license. Contributions are welcomed and appreciated.