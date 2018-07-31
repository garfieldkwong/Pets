"""Adoption handler"""
from orm import customers, matches, pets
from ..base import json_handler
from .. import error
from ..error import handler as error_handler


class Handler(json_handler.JSONHandler):
    """Base handler"""
    @error_handler.coroutine
    def post(self, customer_id):
        pet_id = self.get_argument('pet_id', None)
        if pet_id is None:
            raise error.MissingInput()
        customer = matches.Match.query_matched_pets(self.db, customer_id, pet_id)
        if customer is None:
            raise error.ResourceNotFound()
        if len(customer.matched_pets) <= 0:
            raise error.ResourceNotFound()
        pet = customer.matched_pets[0]
        customer.adopted_pets.append(pet)
        customer.matched_pets.remove(pet)
        pet.matched_customers.remove(customer)
        self.db.commit()
