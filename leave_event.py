# leave_event.py

import falcon
import json
from constants import *

class LeaveEvent(object):

    def on_post(
        self,
        req: falcon.Request,
        resp: falcon.Response,
        event_id: str,
        person_id: str
    ):
        conn.srem(event_id + ':people', person_id)
        conn.srem('person:' + person_id, event_id)
        resp.status = falcon.HTTP_200