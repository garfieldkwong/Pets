"""Pets handler"""
from datetime import datetime
from orm import pets
from ..matches import base
from ..error import handler


class Handler(base.Handler):
    """Pet handler"""
    json_schema = {
        'POST': (__package__, 'post_schema.json'),
        'PUT': None,
    }

    @handler.coroutine
    def post(self, *args, **kwargs):
        """Post handler"""
        pet_data = self.request.arguments['data'][0]
        pet = pets.Pet(
            name=pet_data['name'],
            available_from = datetime.fromtimestamp(
                pet_data['available_from']
            ),
            age=pet_data['age'],
            species=pet_data['species'],
        )
        if pet.has_breed:
            pet.breed = pet_data.get('breed', None)
        self.db.add(pet)
        self.db.commit()
        self.write_pets([pet])

        # try matching after sent response
        self.match_adding_pet(pet)

    @handler.coroutine
    def get(self, id=None):
        """Get handler"""
        if id is None:
            self.write_pets(self.db.query(pets.Pet).all())
        else:
            self.write_pets(self.db.query(pets.Pet).filter(pets.Pet.id == id).all())
