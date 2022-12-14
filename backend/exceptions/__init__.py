class NotFound(Exception):
    """
    Not found
    """


class UniqueViolationError(Exception):
    """
    Unique Violation Error
    """


class IllegalInput(Exception):
    """
    Input is not legal
    """


class LoginExpired(Exception):
    """
    Jwt token is expired
    """
