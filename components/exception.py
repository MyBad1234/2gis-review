class ModeException(Exception):
    """error if browser mode is not set"""

    pass


class ProxyError(Exception):
    """if proxy is incorrect"""

    pass


class SelectExceptions(Exception):
    """exception for select sql query"""

    pass


class UpdateExceptions(Exception):
    """exception for update query"""

    pass


class InsertExceptions(Exception):
    """exception for insert query"""

    pass
