
class PassRotateException(Exception):
    pass


class PrepareException(PassRotateException):
    pass


class ExecuteException(Exception):
    pass