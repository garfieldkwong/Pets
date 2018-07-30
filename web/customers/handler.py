"""Pets handler"""
import json
from orm import customers
from ..base import json_handler as json_base
from ..error import handler


class Handler(json_base.JSONHandler):
    """Pet handler"""
    json_schema = {
        'POST': (__package__, 'post_schema.json'),
        'PUT': None,
    }

    @handler.coroutine
    def post(self, *args, **kwargs):
        """Post handler"""
        customer = customers.Customer()
        preference_data = self.request.arguments['data'][0]['preference']
        customer.preference_age.append(
            customers.PreferenceAge(
                min=preference_data['age'].get('min', None),
                max=preference_data['age'].get('max', None),
            )
        )
        for species in preference_data['species']:
            customer.preference_species.append(
                customers.PreferenceSpecies(
                    name=species
                )
            )
        for breed in preference_data['breed']:
            customer.preference_breed.append(
                customers.PreferenceBreed(
                    name=breed
                )
            )
        self.db.add(customer)
        self.db.commit()
        self.write_customers([customer])

    @handler.coroutine
    def get(self, id=None):
        """Get handler"""
        result = customers.Customer.query_customers_by_id(self.db, id)
        self.write_customers(result)

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
