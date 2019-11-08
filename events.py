import falcon
import json

from constants import *

# Each resource class goes in its own file
# TODO: Proper docstrings, error handling

class Events(object):
    """
    methods:

    on_post(): Take in event data and send appropriate commands to Redis.
    on_get(): Retrieve event data from Redis.
    """

    def __post_event(self, category: str, event: dict):
        """
        Create an event in Redis.
        args:
        event    Dictionary mapping event fields to content.
        """
        # TODO: Can efficiency be improved with Redis pipelining?
        # TODO: Should these operations be grouped in a Redis transaction?
        # TODO: Error handling
        # Creates a hash representation of the event in Redis
        status = conn.hmset(event['id'], event)
        # Add this event's id to the set of all events in the category
        conn.sadd('event-categories:'+ category, event['id'])

    def on_get(
        self,
        req: falcon.Request,
        resp: falcon.Response,
        category: str
        ):
        """
        Send a response containing data for all events in JSON format.
        """
        if category == None: # We don't have a list of valid categories to check.
            raise falcon.HTTPNotFound()
        # Get the IDs for all events in the category
        event_ids = conn.smembers('event-categories:' + category)
        # Retrieve event data and package into a JSON document
        events = {}
        for event_id in event_ids:
            event_data = self.__get_events(event_id)
            events[event_id] = event_data
        resp.status = falcon.HTTP_200
        resp.body = (json.dumps(events))


    def on_post(
        self,
        req: falcon.Request,
        resp: falcon.Response,
        category: str
        ):
        """
        Given a POST request containing event data, create the event in Redis.
        """
        # Read the request as a dict.
        event_data = req.media
        # Ensure request contains all required fields.
        # Doesn't currently prevent user from entering extra fields.
        if (not self.__is_valid_event(event_data)):
            raise falcon.HTTPBadRequest()
        #Assign a unique id to this event
        event_data['id'] = self.__generate_event_id()
        self.__post_event(category, event_data)
        resp.status = falcon.HTTP_200

    def __is_valid_event(self, event: dict):
        """Return True if event contains the required fields, false otherwise."""
        return all(required_field in event.keys() for required_field in event_required_fields)

    def __get_events(self, event_id: str):
        """Return event data as a dictionary."""
        return conn.hgetall(event_id)

    def __generate_event_id(self):
        """Return a new unique event id as a string of the form event:number."""
        generated_id = conn.incr('event_id')
        return 'event:' + str(generated_id)

