# beta.py
import falcon

class BetaLinkResource(object):
    def on_get(
        self,
        req: falcon.Request,
        resp: falcon.Response):
        resp.status = falcon.HTTP_200
        resp.body = (r'https://l.facebook.com/l.php?u=https%3A%2F%2Ftestflight.apple.com%2Fjoin%2Fe05hgsxP%3Ffbclid%3DIwAR2Trl0qZ9pFvEaKjQq2aVvAwJC8IwjPUaEGrJJWls1HiER2MgjE-wCw0MM&h=AT0wLWiDwm-vJfx4nsCfaZWZWXp7G-waPLjtXWsGho7OC8J5Y_zQUn8QkLozVo9qzRKkXt0rEf-Wi0lafOxGvx60zH3cZkLYR_e73hAXQb_kwLXx3hcu1-0STMPMoKyZ7QFQ')