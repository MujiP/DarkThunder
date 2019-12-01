# join_event.py

import falcon
import json
from constants import *
from events import get_event_data, get_people

class JoinEvent(object):

    def on_post(
        self,
        req: falcon.Request,
        resp: falcon.Response,
        event_id: str,
        person_id: str
    ):
        '''
        Add a person to an event.

        HTTP response codes:
        200 if successful
        404 if event doesn't exist
        403 if event is at its max occupancy
        '''
        event_data = get_event_data(event_id)
        if event_data == {}:
            resp.status = falcon.HTTP_404
        elif 'maxOccupancy' in event_data and (
            len(get_people(event_id)) >= int(event_data['maxOccupancy'])
            ):
            resp.status = falcon.HTTP_403
            resp.content_type = 'text/html'
            resp.body = '''
                <html>
                    <head>
                        <title>Forbidden</title>
                    </head>
                    <body>
                        <h1><p>The requested event has reached its maximum occupancy.</p></h1>
                        
                    </body>
                </html>
                '''

        else:
            conn.sadd(event_id + ':people', person_id)
            conn.sadd('person:' + person_id, event_id)
            resp.status = falcon.HTTP_200