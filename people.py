# people.py

import falcon
import json
from events import list_events
from constants import *

class People(object):

    def on_get(
        self,
        req: falcon.Request,
        resp: falcon.Response,
        person_id: str
        ):
        event_ids = list(conn.smembers('person:' + person_id))
        events = []
        if len(event_ids) > 0:
            json_body = list_events(event_ids)
            resp.status = falcon.HTTP_200
            resp.body = (json.dumps(json_body))
        else:
            resp.status = falcon.HTTP_404