from orm import matches
from . import base
from .. import error
from ..error import handler as error_handler


class Handler(base.Handler):
    """Match pets handler"""
    @error_handler.coroutine
    def get(self, pet_id=None):
        """Get handler"""
        if pet_id is None:
            raise error.MissingInput()
        pet = matches.Match.query_matched_customers(self.db, pet_id)
        if pet is None:
            raise error.ResourceNotFound()
        self.write_customers(pet.matched_customers)
