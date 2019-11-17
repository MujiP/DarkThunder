import falcon
from events import Events
from beta import BetaLinkResource

# Connect all the resources to their endpoints.
# This file is a nice place to see the whole API

api = falcon.API()
api.add_route('/events/{category}', Events())
api.add_route('/beta', BetaLinkResource())

# Whatever is passed in place of {category} enters as a variable