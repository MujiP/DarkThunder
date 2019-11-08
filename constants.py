import redis

# A nice place to put some constants,
# and to store a redis connection

conn = redis.Redis(
    #host='...',
    #port=1234,
    #password='...',
    decode_responses=True
)

event_required_fields = ['name', 'location', 'start_time', 'end_time']
event_optional_fields = ['description']