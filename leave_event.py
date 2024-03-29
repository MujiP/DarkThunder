# leave_event.py

import falcon
import json
from constants import *
from events import get_event_data

class LeaveEvent(object):

    def on_post(
        self,
        req: falcon.Request,
        resp: falcon.Response,
        event_id: str,
        person_id: str
    ):
        event_data = get_event_data(event_id)
        if event_data == {}:
            resp.status = falcon.HTTP_404
        else:
            conn.srem(event_id + ':people', person_id)
            conn.srem('person:' + person_id, event_id)
            resp.status = falcon.HTTP_200