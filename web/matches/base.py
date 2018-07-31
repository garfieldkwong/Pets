"""Matchess handler"""
import json
from orm import customers, pets
from ..base import json_handler
from ..error import handler
from ..notification import handler as ws_handler


class Handler(json_handler.JSONHandler):
    """Matches """
    @handler.coroutine
    def get(self):
        """Get handler"""
        pass

    def write_matches(self, matches_list):
        """Write matches"""
        pass

    def match_adding_pet(self, adding_pet):
        """Match the adding pet"""
        result = customers.Customer.query_with_preference(
            self.db, adding_pet.age, adding_pet.species, adding_pet.breed
        )
        for item in result:
            item.matched_pets.append(adding_pet)
            adding_pet.matched_customers.append(item)
        self.db.commit()
        for item in result:
            session = ws_handler.sessions.get(item.id, None)
            if session is not None:
                session.write_message(
                    json.dumps({
                        'type': 'pet',
                        'data': self.get_output_data(adding_pet)
                    })
                )


    def match_adding_customer(self, adding_customer):
        """Match the adding customer"""
        species_list = []
        for item in adding_customer.preference_species:
            species_list.append(item.name)
        breed_list = []
        for item in adding_customer.preference_breed:
            breed_list.append(item.name)
        result = pets.Pet.query_with_perference(
            self.db,
            adding_customer.preference_age[0].min,
            adding_customer.preference_age[0].max,
            species_list if len(species_list) > 0 else None,
            breed_list if len(breed_list) > 0 else None,
        )
        for item in result:
            adding_customer.matched_pets.append(item)
            item.matched_customers.append(adding_customer)
        self.db.commit()

    def get_output_data(self, pet):
        """Get output data of per pet"""
        return {
            'id': pet.id,
            'name': pet.name,
            'available_from': pet.available_from.timestamp(),
            'age': pet.age,
            'species': pet.species,
            'breed': pet.breed,
        }

    def write_pets(self, pets):
        """Write pets data"""
        data = []
        for pet in pets:
            data.append(self.get_output_data(pet))
        self.write(json.dumps(
            {
                'data': data
            }
        ))

    def write_customers(self, customers_list):
        """Write pets data"""
        data = []
        for customer in customers_list:
            species_list = []
            for species in customer.preference_species:
                species_list.append(species.name)
            breed_list = []
            for breed in customer.preference_breed:
                breed_list.append(breed.name)
            data.append({
                'id': customer.id,
                'preference': {
                    'age': {
                        'min': customer.preference_age[0].min,
                        'max': customer.preference_age[0].max
                    },
                    'species': species_list,
                    'breed': breed_list
                }
            })

        self.write(json.dumps(
            {
                'data': data
            }
        ))

