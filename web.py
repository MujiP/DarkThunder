import falcon
from events import Events
from people import People
from join_event import JoinEvent
from leave_event import LeaveEvent
# Connect all the resources to their endpoints.
# This file is a nice place to see the whole API

api = falcon.API()
api.add_route('/events', Events()) # All events; GET to list all and POST to create
api.add_route('/events/{person_id}', People()) # Events a person is part of; GET
api.add_route('/join/{event_id}/{person_id}', JoinEvent()) # Add a person to an event; POST
api.add_route('/leave/{event_id}/{person_id}', LeaveEvent()) # Remove a person from an event; POST