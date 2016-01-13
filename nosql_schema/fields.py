from validators import *


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


class NumberField(Field):
    validators = [Validator, NumberValidator, MinValidator, MaxValidator, RangeValidator]

    def __init__(self, **kwargs):
        Field.__init__(self, **kwargs)

        try:
            self.min = kwargs.pop('min')
        except KeyError:
            self.min = None

        try:
            self.max = kwargs.pop('max')
        except KeyError:
            self.max = None

        try:
            self.range = kwargs.pop('range')
        except KeyError:
            self.range = None


class StringField(Field):
    validators = [Validator, StringValidator, StringMinValidator, StringMaxValidator, RegexpValidator]

    def __init__(self, **kwargs):
        Field.__init__(self, **kwargs)

        try:
            self.min = kwargs.pop('min')
        except KeyError:
            self.min = None

        try:
            self.max = kwargs.pop('max')
        except KeyError:
            self.max = None

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


class DictField(Field):
    validators = [Validator, DictValidator]

    def __init__(self, **kwargs):
        Field.__init__(self, **kwargs)

        try:
            self.allowed_fields = kwargs.pop('allowed_fields')
        except KeyError:
            self.allowed_fields = None


class ListField(Field):
    validators = [Validator, ListValidator]

    def __init__(self, **kwargs):
        Field.__init__(self, **kwargs)

        try:
            self.allowed_values = kwargs.pop('allowed_values')
        except KeyError:
            self.allowed_values = None
