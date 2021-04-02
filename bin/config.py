""" Application configuration

The configuration is loaded from the environment variables, you may
override them "manually" or via a ``.env`` file located in the current
directory. Alternativaly you can use the ``--rtdbin-config`` command line
option to define a dotenv to load instead of ``./.env``.

It tries to correctly configure logging according to the server software
you are using

The options are:

* ``RTDBIN_HOST``: The HTTP address the embedded server binds (default: localhost)
* ``RTDBIN_PORT``: The HTTP port the embedded server binds (default: 8012)
* ``RTDBIN_MAXSIZE``: The maximum ``Content-Length`` accepted for new snippets (default: 16kiB)
* ``RTDBIN_IDENTSIZE``: The length of generated unique identifier for new snippets (default: 6)
* ``RTDBIN_DEFAULT_LANGUAGE``: The default language selected in the new snippet form
* ``RTDBIN_DEFAULT_MAXUSAGE``: The default maximum usages before a snippet is automatically removed, 0 means no maximum (default: 0)
* ``RTDBIN_DEFAULT_LIFETIME``: The default time before a snippet is automatically removed, 0 means no limit (default: 0)
* ``REDIS_HOST``: The Redis host adress to connect to
* ``REDIS_PORT``: The Redis port to connect to
* ``REDIS_DB``: The Redis database to connect to
"""


import logging
import os
from argparse import ArgumentParser
from dotenv import load_dotenv
from metrics import Byte, Time


logger = logging.getLogger(__name__)
bin_logger = logging.getLogger(__package__)


def strtobool(s):
    try:
        s = s.lower()
    except AttributeError:
        pass
    return s not in {False, "0", "false", "no"}


def _setup():
    global HOST, PORT, MAXSIZE, IDENTSIZE
    global DEFAULT_LANGUAGE, DEFAULT_MAXUSAGE, DEFAULT_LIFETIME
    global REDIS_HOST, REDIS_PORT, REDIS_DB

    cli = ArgumentParser()
    cli.add_argument('--rtdbin-port', metavar="PORT", type=int, help="builtin server port")
    cli.add_argument('--rtdbin-config', metavar="PATH", help="dotenv config file")
    options = cli.parse_known_args()[0]
    load_dotenv(options.rtdbin_config)  # use a sensitive default when omitted

    server_software = os.getenv("SERVER_SOFTWARE", "")  # Set by WSGI servers

    # Extact configuration from environ
    if server_software == "":
        HOST = os.getenv('RTDBIN_HOST', 'localhost')
        PORT = options.rtdbin_port or int(os.getenv('RTDBIN_PORT', 8012))
    MAXSIZE = Byte(os.getenv('RTDBIN_MAXSIZE', '16kiB'))
    IDENTSIZE = int(os.getenv('RTDBIN_IDENTSIZE', 6))
    DEFAULT_LANGUAGE = os.getenv('RTDBIN_DEFAULT_LANGUAGE', 'text')
    DEFAULT_MAXUSAGE = int(os.getenv('RTDBIN_DEFAULT_MAXUSAGE', 0))
    DEFAULT_LIFETIME = Time(os.getenv('RTDBIN_DEFAULT_LIFETIME', 0))
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    REDIS_DB = int(os.getenv('REDIS_DB', 0))

    # Configure logging
    if "gunicorn" in server_software:
        gunicorn_logger = logging.getLogger('gunicorn.error')
        bin_logger.handlers = gunicorn_logger.handlers
        bin_logger.setLevel(gunicorn_logger.level)
    elif server_software == "":
        logging.basicConfig(level='DEBUG')
    else:
        logger.warning(
            "Unknown WSGI server: %s, logging may not work as intended.",
            server_software
        )

    # Report config
    logger.debug(
        "Detected WSGI server: %s.",
        server_software or 'builtin wsgiref (unsafe for production)'
    )
    logger.debug(
        "Runtime configuration:\n  %s", "\n  ".join([
        f"{key}: {val}" for key, val in globals().items()
        if key.isupper() and not key.startswith('__')
    ]))

_setup()
