import redis
from urllib.parse import urlparse

# A nice place to put some constants,
# and to store a redis connection
url = urlparse(os.environ.get('REDISCLOUD_URL'))
conn = redis.Redis(
    host=url.hostname, 
    port=url.port, 
    password=url.password,
    decode_responses=True
)

event_required_fields = ['name', 'location', 'start_time', 'end_time']
event_optional_fields = ['description']