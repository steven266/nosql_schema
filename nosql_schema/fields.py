"""
This module contains the Field-class definitions
"""

from .validators import *
from .exceptions import PasswordFuncError


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

        try:
            self.post_processors = kwargs.pop('post_processors')

            if type(self.post_processors) is not list:
                self.post_processors = [self.post_processors]
        except KeyError:
            self.post_processors = None

    def process(self, value=None):
        if type(self.post_processors) is not list:
            return value

        for processor in self.post_processors:
            if hasattr(processor, '__call__'):
                value = processor(value=value)

        return value

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


class DateField(NumberField):
    validators = [Validator, NumberValidator, MinValidator, MaxValidator, RangeValidator]


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


class PasswordField(StringField):
    def __init__(self, **kwargs):
        try:
            post_processors = kwargs.pop('post_processors')
            if type(self.post_processors) is not list:
                self.post_processors = [self.post_processors]
        except KeyError:
            post_processors = []

        try:
            min_len = min(5, kwargs.pop('min'))
        except KeyError:
            min_len = 5

        try:
            max_len = max(min_len, kwargs.pop('max'))
        except KeyError:
            max_len = None

        try:
            password_func = kwargs.pop('password_func')
        except KeyError:
            raise PasswordFuncError('Parameter "password_func" is mandatory!')

        post_processors.append(password_func)

        StringField.__init__(self, post_processors=post_processors, min=min_len, max=max_len, **kwargs)


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
