"""The routes for web server
POST /pets
Add a new pet to the system, with all the properties described above

GET /pets/{id}
Fetch the pet by ID

GET /pets/{id}/matches
Get an array of "matching" customers for the given pet

POST /customers
Add a new customer to the system

Together with their preferences for pets

GET /customers/{id}
Fetch the customer by ID

GET /customers/{id}/matches
Get an array of "matching" Pets for the given customer

POST /customers/{id}/adopt?pet_id={pet_id}
The Customer adopts the given Pet

The Pet and Customer should no longer appear in /matches queries
"""
import os
from tornado import web
from web.adoptions import handler as adoption_handler
from web.customers import handler as customer_handler
from web.matches import match_pets, match_customer
from web.notification import handler as notification_handler
from web.pets import handler as pets_handler


URLs = [
    (r"/pets", pets_handler.Handler),
    (r"/pets/?([0-9]*)?", pets_handler.Handler),
    (r"/customers", customer_handler.Handler),
    (r"/customers/?([0-9]*)?", customer_handler.Handler),
    (r"/customers/([0-9]*)/matches", match_pets.Handler),
    (r"/pets/([0-9]*)/matches", match_customer.Handler),
    (r"/customers/([0-9]*)/adopt", adoption_handler.Handler),
    (r"/ws/([0-9]*)", notification_handler.WebsocketHandler),
    (  # Javascript handler
        r"/static/(.*)", web.StaticFileHandler, {
            'path': os.path.join(
                os.path.dirname(__file__), 'web', 'static',
            )
        }
    )
]
