from orm import matches
from . import base
from .. import error
from ..error import handler as error_handler


class Handler(base.Handler):
    """Match pets handler"""
    @error_handler.coroutine
    def get(self, customer_id=None):
        """Get handler"""
        if customer_id is None:
            raise error.MissingInput()
        customer = matches.Match.query_matched_pets(self.db, customer_id)
        if customer is None:
            raise error.ResourceNotFound()
        self.write_pets(customer.matched_pets)
