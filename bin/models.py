from redis import Redis
from genpw import pronounceable_passwd
from bin import config


database = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)


class Snippet:
    def __init__(self, ident, code, views_left):
        self.id = ident
        self.code = code
        self.views_left = views_left

    @classmethod
    def create(cls, code, maxusage, lifetime):
        ident = pronounceable_passwd(6)
        database.hset(ident, "code", code)
        database.hset(ident, "views_left", maxusage)
        if lifetime > 0:
            database.expire(ident, int(lifetime))
        return cls(ident, code, maxusage)

    @classmethod
    def get_by_id(cls, snippet_id):
        snippet = database.hgetall(snippet_id)

        if not snippet:
            raise KeyError('Snippet not found')

        code = snippet[b'code'].decode('utf-8')
        views_left = int(snippet[b'views_left'].decode('utf-8'))
        if views_left == 0:
            pass
        elif views_left == 1:
            database.delete(snippet_id)
        else:
            database.hincrby(snippet_id, 'views_left', -1)

        return cls(snippet_id, code, views_left)
