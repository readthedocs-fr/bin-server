import textwrap
import itertools
from redis import Redis
from genpw import pronounceable_passwd

database = Redis(host='localhost', port=6379)

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
