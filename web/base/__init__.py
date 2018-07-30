"""Base handler"""
import logging
import json
from tornado import web


class Base(web.RequestHandler):
    """Base handler"""
    debug_api = False
    logger = logging.getLogger(__name__)

    @property
    def db(self):
        return self.application.db

    def handler_error(self, exc):
        """Handler error"""
        if self.debug_api:
            self.logger.exception(exc)
        if exc.http_status != 200:
            self.set_status(exc.http_status)
            self.write_error(exc.http_status, json_error=exc)
        else:
            self.write(json.dumps({
                'status': exc.error_code,
                'output': exc.construct_msg()
            }))

    def write_error(self, status_code, **kwargs):
        """Customized error page"""
        if 'json_error' in kwargs:  # Write JSON instead
            if self.debug_api:
                self.logger.exception(kwargs['json_error'])
            err_msg = {
                'status': kwargs['json_error'].error_code,
            }
            err_output = kwargs['json_error'].construct_msg()
            if len(err_output) > 0:
                err_msg['output'] = err_output
            self.write(json.dumps(err_msg))
        else:  # Unexpected - use default
            super().write_error(status_code, **kwargs)
