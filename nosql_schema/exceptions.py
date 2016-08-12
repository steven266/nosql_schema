"""
This module contains Error-class definitions
"""


class ValidationError(Exception):
    def __init__(self, message,):
        super(ValidationError, self).__init__(message)


class PasswordFuncError(Exception):
    def __init__(self, message,):
        super(PasswordFuncError, self).__init__(message)
