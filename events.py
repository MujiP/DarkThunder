import falcon
import json

from constants import *

# Each resource class goes in its own file
# TODO: Proper docstrings, error handling

class Events(object):
    """
    Events resource of our API, for posting and getting events.

    Raises exceptions:
    falcon.HTTPNotFound (404 Not Found)
    falcon.HTTPBadRequest (400 Bad Request)

    Methods:
    on_post(): 
    on_get(): 
    """

    def __post_event(self, category: str, event: dict):
        """
        Create an event in Redis.

        Arguments:
        category -- Event category.
        event -- Dictionary mapping event fields to content.
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
        Falcon responder for HTTP get method.
        Send an HTTP response containing data for all events 
        in the given category. Repsonse is in JSON format.

        Arguments:
        req -- Incoming HTTP request.
        resp -- Outgoing HTTP response. 404 if no category given.
        category -- Category from which to get events.
        """
        # We don't have a list of valid categories to check,
        # so just make sure there is a category.
        if category == '': 
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
        Falcon responder for HTTP post method.
        Given a request containing event data, create the event in Redis.

        Arguments:
        req --  Incoming HTTP request. Media attribute must be a JSON 
                object containing all required event fields. 
        resp -- Outgoing HTTP response. 404 if no category given,
                400 if JSON object is missing required fields.
        category -- Category to post the event to.
        """
        # We don't have a list of valid categories to check,
        # so just make sure there is a category.
        if category == '':
            raise falcon.HTTPNotFound()
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

