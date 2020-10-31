import textwrap
import itertools
from redis import Redis
from genpw import pronounceable_passwd
from bin import config


if config.REDIS_ENABLED:
    database = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)
else:
    print("Using dummy in-memory database")
    class database:
        db = {}

        @classmethod
        def set(cls, ident, code):
            cls.db[ident] = code.encode()

        @classmethod
        def get(cls, ident):
            return cls.db.get(ident)

class Snippet:
    def __init__(self, ident, code):
        self.id = ident
        self.code = code

    @classmethod
    def create(cls, code):
        ident = pronounceable_passwd(6)
        database.set(ident, code)
        return cls(ident, code)

    @classmethod
    def get_by_id(cls, snippet_id):
        code = database.get(snippet_id)
        if not code:
            raise KeyError('Snippet not fond')
        return cls(snippet_id, code.decode('utf-8'))
