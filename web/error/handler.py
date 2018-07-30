"""Error handler"""
from tornado import gen
from .. import error


def coroutine(func):
    """Error coroutine decorator"""
    @gen.coroutine
    def wrapper(self, *args, **kwargs):
        """Wrapper"""
        try:
            yield gen.coroutine(func)(self, *args, **kwargs)
        except (error.BaseError) as exc:
            return self.handle_error(exc)
    return wrapper
