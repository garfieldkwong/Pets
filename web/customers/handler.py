"""Pets handler"""
from orm import customers
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

        # try matching after sent response
        self.match_adding_customer(customer)

    @handler.coroutine
    def get(self, id=None):
        """Get handler"""
        result = customers.Customer.query_with_id(self.db, id)
        self.write_customers(result)
