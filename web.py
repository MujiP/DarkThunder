import falcon
from events import Events
from people import People

# Connect all the resources to their endpoints.
# This file is a nice place to see the whole API

api = falcon.API()
api.add_route('/events', Events()) # All events; GET and POST
api.add_route('/events/{person_id}', People()) # Events a person is part of; GET
#api.add_route('/join/{event_id}/{person_id}', ) # Add a person to an event; POST
#apie.add_route('/leave/{event_id}/{person_id}', ) # Remove a person from an event; 


# Whatever is passed in place of {category} enters as a variable