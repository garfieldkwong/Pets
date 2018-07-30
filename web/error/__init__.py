"""errors"""


class BaseError(Exception):
    """Base error class"""
    https_status = 500
    error_code = 500
    msg_prefix = ''

    def __init__(self, msg='', **kwargs):
        """Error with an optional error message"""
        super().__init__(msg)
        self.msg = msg
        for key, value in kwargs.items():
            setattr(self, key, value)

    def construct_msg(self):
        """Construct error message"""
        if len(self.msg) > 0 and len(self.msg_prefix) > 0:
            seq = ': '
        else:
            seq = ''
        return self.msg_prefix + seq + self.msg

    def __str__(self):
        """Return string representing the error"""
        return self.construct_msg()


class ValidationError(BaseError):
    """Data validation error.
    Web sematics: Invalid input (bad request)
    """
    https_status = 400
    error_code = 400
