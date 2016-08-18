import unittest
import os
from nosql_schema import fields, schema, exceptions

# Configure database
schema.Schema.__config__ = {
    'database': 'nosqlite',
    'path': './database.db'
}


class TestFields(unittest.TestCase):
    def test_field(self):
        # Test required
        field = fields.Field(required=False)
        self.assertTrue(field.validate(value=None))

        field = fields.Field()
        self.assertFalse(field.validate(value=None))

    def test_number_field(self):
        # Test number field
        # int
        field = fields.NumberField()
        self.assertTrue(field.validate(value=int(1)))

        # float
        field = fields.NumberField()
        self.assertTrue(field.validate(value=float(1)))

        # long
        field = fields.NumberField()
        self.assertTrue(field.validate(value=long(1)))

        # other
        field = fields.NumberField()
        self.assertFalse(field.validate(value=str(1)))

        # min
        field = fields.NumberField(min=10)
        self.assertFalse(field.validate(value=1))

        field = fields.NumberField(min=10)
        self.assertTrue(field.validate(value=10))

        # max
        field = fields.NumberField(max=10)
        self.assertFalse(field.validate(value=11))

        field = fields.NumberField(max=10)
        self.assertTrue(field.validate(value=10))

        # range
        field = fields.NumberField(range=range(0, 10, 2)) # 0, 2, 4, 6, 8
        self.assertFalse(field.validate(value=1))

        field = fields.NumberField(range=range(0, 10, 2))
        self.assertTrue(field.validate(value=4))

    def test_string_field(self):
        # Test string fields
        field = fields.StringField()
        self.assertFalse(field.validate(value=1))

        field = fields.StringField()
        self.assertTrue(field.validate(value='Hello World'))

    def test_email_field(self):
        # regular expression -> EmailField
        field = fields.EmailField()
        self.assertFalse(field.validate(value='Hello World'))

        field = fields.EmailField()
        self.assertTrue(field.validate(value='example@example.com'))

    def test_choice_field(self):
        # ChoiceField
        field = fields.ChoiceField(choices=['foo', 'bar'])
        self.assertFalse(field.validate(value='Hello World'))

        field = fields.ChoiceField(choices=['foo', 'bar'])
        self.assertTrue(field.validate(value='foo'))

        field = fields.ChoiceField(choices=['foo', 'bar'])
        self.assertFalse(field.validate(value='Hello World'))

        field = fields.ChoiceField(choices=['foo', 'bar'])
        self.assertTrue(field.validate(value='foo'))

    def test_dict_field(self):
        # DictField
        field = fields.DictField()
        self.assertFalse(field.validate(value='Hello World'))

        field = fields.DictField()
        self.assertTrue(field.validate(value={'foo': 'bar'}))

        field = fields.DictField(allowed_fields={
            'id': fields.NumberField(min=0),
            'name': fields.StringField(),
            'email': fields.EmailField(),
        })
        self.assertTrue(field.validate(value={'foo': 'bar'}))

        field = fields.DictField(allowed_fields={
            'id': fields.NumberField(min=0),
            'name': fields.StringField(),
            'email': fields.EmailField(),
        })
        self.assertTrue(field.validate(value={
            'id': 2,
            'name': 'John Doe',
            'email': 'john.doe@example.com'
        }))

    def test_list_field(self):
        # ListField
        field = fields.ListField()
        self.assertFalse(field.validate(value='Hello World'))

        field = fields.ListField()
        self.assertTrue(field.validate(value=['foo', 'bar']))

        field = fields.ListField(allowed_values=['foo', 'bar'])
        self.assertFalse(field.validate(value=['baz']))

        field = fields.ListField(allowed_values=['foo', 'bar'])
        self.assertTrue(field.validate(value=['foo']))


class TestNoSQLSchema(unittest.TestCase):
    class MyTestSchema(schema.Schema):
        name = fields.StringField()
        email = fields.EmailField()

    def test_schema(self):
        self.assertTrue(TestNoSQLSchema.MyTestSchema.count() == 0)

        obj = TestNoSQLSchema.MyTestSchema(name='John Doe', email='john.doe@example.com')
        obj.save()

        id = obj._id

        self.assertTrue(TestNoSQLSchema.MyTestSchema.count() == 1)
        self.assertIsNotNone(obj._id)

        obj.name = 'Jane Doe'
        obj.save()

        obj = TestNoSQLSchema.MyTestSchema.find_one({'_id': id})
        self.assertIsNotNone(obj)

        self.assertTrue(obj.name == 'Jane Doe')

        result = TestNoSQLSchema.MyTestSchema.find(offset=1)
        self.assertEqual(result, [])

        obj.delete()
        self.assertTrue(TestNoSQLSchema.MyTestSchema.count() == 0)

        try:
            obj = TestNoSQLSchema.MyTestSchema(name='John Doe', email='john')
            obj.save()
        except exceptions.ValidationError:
            pass

        self.assertTrue(TestNoSQLSchema.MyTestSchema.count() == 0)

    def tearDown(self):
        # remove database
        filename = schema.Schema.__config__['path']
        try:
            os.remove(filename)
        except OSError:
            pass


if __name__ == '__main__':
    unittest.main()
