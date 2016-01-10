from validators import Validator, StringValidator, RegexpValidator, ChoiceValidator, DictValidator, ListValidator


class Field:
    validators = [Validator]

    def __init__(self, **kwargs):
        try:
            self.required = kwargs.pop('required')
        except KeyError:
            self.required = True

        try:
            self.default = kwargs.pop('default')
        except KeyError:
            self.default = None

    def validate(self, value=None):
        valid = True

        for validator in self.validators:
            valid = valid and validator.validate(value=value, field=self)

        return valid


# TODO: implement
class NumberField(Field):
    pass


class StringField(Field):
    validators = [Validator, StringValidator, RegexpValidator]

    def __init__(self, **kwargs):
        Field.__init__(self, **kwargs)

        try:
            self.regexp = kwargs.pop('regexp')
        except KeyError:
            self.regexp = None


class EmailField(StringField):
    def __init__(self, **kwargs):
        StringField.__init__(self, regexp=r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", **kwargs)


class ChoiceField(StringField):
    validators = [Validator, StringValidator, RegexpValidator, ChoiceValidator]

    def __init__(self, **kwargs):
        StringField.__init__(self, **kwargs)

        try:
            self.choices = kwargs.pop('choices')
        except KeyError:
            self.choices = None


# TODO: implement 'allowed_fields'
class DictField(Field):
    validators = [Validator, DictValidator]


# TODO: implement 'allowed_values'
class ListField(Field):
    validators = [Validator, ListValidator]
