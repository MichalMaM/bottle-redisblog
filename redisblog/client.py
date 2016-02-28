from . import settings

from redis import Redis

client = Redis(**getattr(settings, 'REDIS_BACKEND'))
