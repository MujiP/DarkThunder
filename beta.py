# beta.py
import falcon
import json

class BetaLinkResource(object):
    def on_get(
        self,
        req: falcon.Request,
        resp: falcon.Response):
        resp.status = falcon.HTTP_200
        beta_link = {'link': r'https://testflight.apple.com/join/e05hgsxP?fbclid=IwAR2Trl0qZ9pFvEaKjQq2aVvAwJC8IwjPUaEGrJJWls1HiER2MgjE-wCw0MM'}
        resp.body = (json.dumps(beta_link))