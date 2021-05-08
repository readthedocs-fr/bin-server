""" Mapping between python objets and the Redis store """


from redis import Redis
from genpw import pronounceable_passwd
from bin import config


# We always connect to Redis
database = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB
)


class Snippet:
    """
    A snippet is a immuable text that have been saved in the database
    and that is retrivable via an unique URL.
    """

    def __init__(self, ident, code, views_left, parentid, token):
        self.id = ident  #: snippet unique identifier
        self.code = code  #: snippet text
        self.views_left = views_left  #: how many time this snippet can be retrieved again
        self.parentid = parentid  #: the original snippet this one is a duplicate of or an empty string
        self.token = token #: the admin token of the snippet

    @classmethod
    def new_id(cls):
        """ Generate a safe unique identifier """
        for _ in range(20):
            ident = pronounceable_passwd(config.IDENTSIZE)

            if len(ident) != config.IDENTSIZE:
                continue
            if ident in {'health', 'assets', 'new', 'raw', 'report'}:
                continue
            if database.exists(ident):
                continue

            return ident

        raise RuntimeError("No free or valid identifier has been found after 20 attempts")


    @classmethod
    def create(cls, code, maxusage, lifetime, parentid, token=None):
        """
        Save a snippet in the database and return a snippet object

        :param code: the source code utf-8 encoded
        :param maxusage: how many times this snippet can be retrieve before self-deletion
        :param lifetime: how long the snippet is saved before self-deletion
        :param parentid: the original snippet id this new snippet is a duplicate of, empty string for original snippet
        :param token: the "admin" token of the snippet, ``None`` if the snippet has no "admin" token
        """
        ident = cls.new_id()
        database.hset(ident, b'code', code)
        database.hset(ident, b'views_left', maxusage)
        database.hset(ident, b'parentid', parentid)
        if token:
            database.hset(ident, b'token', token)
        if lifetime > 0:
            database.expire(ident, int(lifetime))
        return cls(ident, code, maxusage, parentid, token)

    @classmethod
    def get_by_id(cls, ident):
        """
        Retrieve a snippet from the database and return a snippet object

        :param ident: the snippet identifier
        :raises KeyError: the snippet does not exist or have been removed
        """
        snippet = database.hgetall(ident)

        if not snippet:
            raise KeyError('Snippet not found')

        code = snippet[b'code'].decode('utf-8')
        views_left = int(snippet[b'views_left'].decode('utf-8'))
        parentid = snippet[b'parentid'].decode('ascii')
        token = snippet.get(b'token', b'').decode() or None
        if views_left == 0:
            pass
        elif views_left == 1:
            database.delete(ident)
        else:
            database.hincrby(ident, 'views_left', -1)

        return cls(ident, code, views_left, parentid, token)

    def delete(self):
        """
        Delete the snippet from the database
        """
        database.delete(self.id)
