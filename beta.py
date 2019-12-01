# beta.py
import falcon
import json

class BetaLinkResource(object):
    def on_get(
        self,
        req: falcon.Request,
        resp: falcon.Response):
        resp.status = falcon.HTTP_302
        resp.content_type = 'text'
        beta_link = r'https://testflight.apple.com/join/e05hgsxP?fbclid=IwAR2Trl0qZ9pFvEaKjQq2aVvAwJC8IwjPUaEGrJJWls1HiER2MgjE-wCw0MM'
        resp.location = beta_link
        resp.body = r'Please follow this link to access the beta: {}'.format(beta_link)