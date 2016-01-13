import re


class Validator:
    def __init__(self, **kwargs):
        pass

    @staticmethod
    def validate(value=None, field=None):
        if not field:
            return False

        if field.required and value is None:
            return False
        return True


class NumberValidator(Validator):
    @staticmethod
    def validate(value=None, field=None):
        # skip all tests if not required and not defined
        if not field.required and value is None:
            return True

        if type(value) is not int and type(value) is not long and type(value) is not float:
            return False

        return True


class StringValidator(Validator):
    @staticmethod
    def validate(value=None, field=None):
        # skip all tests if not required and not defined
        if not field.required and value is None:
            return True

        if type(value) is not str and type(value) is not unicode:
            return False

        return True


class MinValidator(Validator):
    @staticmethod
    def validate(value=None, field=None):
        # skip all tests if not required and not defined
        if not field.required and value is None:
            return True

        if field.min and value < field.min:
            return False

        return True


class MaxValidator(Validator):
    @staticmethod
    def validate(value=None, field=None):
        # skip all tests if not required and not defined
        if not field.required and value is None:
            return True

        if field.max and value > field.max:
            return False

        return True


class RangeValidator(Validator):
    @staticmethod
    def validate(value=None, field=None):
        # skip all tests if not required and not defined
        if not field.required and value is None:
            return True

        if field.range and value not in field.range:
            return False

        return True


class StringMinValidator(Validator):
    @staticmethod
    def validate(value=None, field=None):
        # skip all tests if not required and not defined
        if not field.required and value is None:
            return True

        if field.min and len(value) < field.min:
            return False

        return True


class StringMaxValidator(Validator):
    @staticmethod
    def validate(value=None, field=None):
        # skip all tests if not required and not defined
        if not field.required and value is None:
            return True

        if field.max and len(value) > field.max:
            return False

        return True


class RegexpValidator(Validator):
    @staticmethod
    def validate(value=None, field=None):
        # skip all tests if not required and not defined
        if not field.required and value is None:
            return True

        if field.regexp:
            pattern = re.compile(field.regexp)
            if not pattern.match(value):
                return False

        return True


class ChoiceValidator(Validator):
    @staticmethod
    def validate(value=None, field=None):
        # skip all tests if not required and not defined
        if not field.required and value is None:
            return True

        if field.choices and value not in field.choices:
            return False

        return True


class DictValidator(Validator):
    @staticmethod
    def validate(value=None, field=None):
        # skip all tests if not required and not defined
        if not field.required and value is None:
            return True

        if not type(value) == dict:
            return False

        if field.allowed_fields:
            for k,v in field.allowed_fields.iteritems():
                if k in value and value[k] is not None and not v.validate(value=value[k]):
                    print v
                    return False

        return True


class ListValidator(Validator):
    @staticmethod
    def validate(value=None, field=None):
        # skip all tests if not required and not defined
        if not field.required and value is None:
            return True

        if not type(value) == list:
            return False

        if field.allowed_values:
            for item in value:
                if item not in field.allowed_values:
                    return False

        return True
