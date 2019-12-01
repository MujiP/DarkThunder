# join_event.py

import falcon
import json
from constants import *

class JoinEvent(object):

    def on_post(
        self,
        req: falcon.Request,
        resp: falcon.Response,
        event_id: str,
        person_id: str
    ):
        conn.sadd(event_id + ':people', person_id)
        resp.status = falcon.HTTP_200