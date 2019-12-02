import falcon
import json

from constants import *

class Events(object):
    """
    Falcon resource for posting and getting events.

    Raises exceptions:
    falcon.HTTPNotFound (404 Not Found)
    falcon.HTTPBadRequest (400 Bad Request)

    Methods:
    on_post(): Post an event to the server.
    on_get(): Retrieve events from the server.
    """

    def __post_event(self, event: dict):
        """
        Create an event in Redis.

        Arguments:
        event -- Dictionary mapping event fields to content.
        """
        # Use a pipeline to group multiple commands in a transaction.
        pipeline = conn.pipeline()
        # Need to create separate tables for the two list fields since hashes can't contain lists.
        if 'people' in event.keys():
            for person in event['people']:
                pipeline.sadd(event['id'] + ':people', person)
                # Add this event to each person's set of events
                pipeline.sadd('person:' + person, event['id'])
            event.pop('people', None)
        if 'tags' in event.keys():
            for tag in event['tags']:
                pipeline.rpush(event['id'] + ':tags', tag)
            event.pop('tags', None)
        # Creates a hash representation of the event in Redis
        status = pipeline.hmset(event['id'], event)
        # Add this event's id to the sorted set of all events (sorted by date)
        pipeline.zadd('date:', {event['id']: event['date']})
        pipeline.rpush('events', event['id'])
        pipeline.execute()

    def on_get(
        self,
        req: falcon.Request,
        resp: falcon.Response
        ):
        """
        Falcon responder for HTTP get method.
        Send an HTTP response containing data for all events 
        in the given category. Repsonse is in JSON format.

        Arguments:
        req -- Incoming HTTP request.
        resp -- Outgoing HTTP response. 404 if no category given.
        """
        # Get the IDs for all events
        event_ids = conn.lrange('events', 0, -1)
        # Retrieve event data and package into a JSON document
        events = list_events(event_ids)
        resp.status = falcon.HTTP_200
        resp.body = (json.dumps(events))

    def on_post(
        self,
        req: falcon.Request,
        resp: falcon.Response
        ):
        """
        Falcon responder for HTTP post method.
        Given a request containing event data, create the event in Redis.

        Arguments:
        req --  Incoming HTTP request. Media attribute must be a JSON 
                object containing all required event fields. 
        resp -- Outgoing HTTP response. 404 if no category given,
                400 if JSON object is missing required fields.
        """
        # Read the request's media as a dictionary.
        event_data = req.media
        # Ensure request contains all required fields.
        # (doesn't currently prevent user from entering extra fields).
        if (not self.__is_valid_event(event_data)):
            raise falcon.HTTPBadRequest()
        #Assign a unique id to this event
        event_data['id'] = self.__generate_event_id()
        self.__post_event(event_data)
        resp.status = falcon.HTTP_200

    def __is_valid_event(self, event: dict):
        """Return True if event contains the required fields, false otherwise."""
        if event == None:
            return False
        return all(required_field in event.keys() 
            for required_field in event_required_fields)


    def __generate_event_id(self):
        """Return a new unique event id as a string of the form event:number."""
        generated_id = conn.incr('event_id')
        return 'event:' + str(generated_id)

def get_people(event_id: str):
    '''Return a list of all people attending an event'''
    return list(conn.smembers(event_id + ':people'))

def get_event_data(event_id: str):
    """Return event data as a dictionary."""
    event_data = conn.hgetall(event_id)
    return event_data

def list_events(event_ids: list):
    '''Return a list containing data for all given events, in order by date'''
    events = []
    i = 0
    for event_id in conn.zrange('date:', 0, -1):
        if event_id in event_ids:
            event_data = get_event_data(event_id)
            events.append(event_data)
            # Look up this event's people in the event:{event_id}:people table
            events[i]['people'] = get_people(event_id)
            # Look up this event's tags in the event:{event_id}:tags table
            events[i]['tags'] = conn.lrange(event_id + ':tags', 0, -1)
            i = i + 1
    return events