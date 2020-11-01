import textwrap
import itertools
from redis import Redis
from genpw import pronounceable_passwd
from bin import config


if config.REDIS_ENABLED:
    database = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)
else:
    raise EnvironmentError('Disabled Redis database is not supported for now')


class Snippet:
    def __init__(self, ident, code, views_left):
        self.id = ident
        self.code = code
        self.views_left = views_left

    @classmethod
    def create(cls, code, maxusage):
        ident = pronounceable_passwd(6)
        database.hset(ident, "code", code)
        database.hset(ident, "views_left", maxusage)
        return cls(ident, code, maxusage)

    @classmethod
    def get_by_id(cls, snippet_id):
        snippet = database.hgetall(snippet_id)
        code = snippet[b'code'].decode('utf-8')
        views_left = snippet[b'views_left'].decode('utf-8')

        if not code:
            raise KeyError('Snippet not fond')

        if views_left != 'inf':
            if int(views_left) - 1 <= 0:
                database.delete(snippet_id)
            else:
                database.hincrby(snippet_id, 'views_left', -1)

        return cls(snippet_id, code, views_left)
