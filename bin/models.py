from redis import Redis
from genpw import pronounceable_passwd
from bin import config
import bottle as bt

database = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB
)

class Snippet:
    def __init__(self, ident, code, views_left, parentid):
        self.id = ident
        self.code = code
        self.views_left = views_left
        self.parentid = parentid

    @classmethod
    def create(cls, code, maxusage, lifetime, parentid):
        for _ in range(20):
            ident = pronounceable_passwd(config.IDENTSIZE)
            if not database.exists(ident):
                break
        else:
            raise RuntimeError("No free identifier has been found after 20 attempts")
        database.hset(ident, b'code', code)
        database.hset(ident, b'views_left', maxusage)
        database.hset(ident, b'parentid', parentid)
        if lifetime > 0:
            database.expire(ident, int(lifetime))
        return cls(ident, code, maxusage, parentid)

    @classmethod
    def get_by_id(cls, ident):
        snippet = database.hgetall(ident)

        if not snippet:
            raise KeyError('Snippet not found')

        code = snippet[b'code'].decode('utf-8')
        views_left = int(snippet[b'views_left'].decode('utf-8'))
        parentid = snippet[b'parentid'].decode('ascii')
        client_ip = bt.request.environ.get('HTTP_X_FORWARDED_FOR') or bt.request.environ.get('REMOTE_ADDR')
        if views_left == 0 or client_ip in config.WHITELISTED_VIEWS:
            pass
        elif views_left == 1:
            database.delete(ident)
        else:
            database.hincrby(ident, 'views_left', -1)

        return cls(ident, code, views_left, parentid)
