import falcon
import json
from constants import *

# Each resource class goes in its own file

class Events:

    def foo(self):
        return "hello world"

    def on_get(
        self,
        req: falcon.Request,
        resp: falcon.Response,
        category: str
        ):

        # Note that we added the category parameter which must match the
        # {category} part of the route we declared in web.py

        if category != "BLAH" category != "AAH":
            # This is how to return an error
            raise falcon.HTTPNotFound()

        # This is how to return data
        resp.body = json.dumps(self.foo())


    def on_post(
        self,
        req: falcon.Request,
        resp: falcon.Response,
        category: str
        ):
        
        # This is how to get the payload that was sent
        dict = req.media
        
        if dict["foobar"] == None or dict["barfoo"] == None:
            raise falcon.HTTPBadRequest()