import os
from argparse import ArgumentParser
from dotenv import load_dotenv
from metrics import Byte, Time

def strtobool(s):
    try:
        s = s.lower()
    except AttributeError:
        pass
    return s not in {False, "0", "false", "no"}

cli = ArgumentParser()
cli.add_argument('port', nargs='?', type=int, default=8012)
cli.add_argument('-c', '--config')
cli.add_argument('--no-redis', dest='redis_enabled', action='store_false')
options = cli.parse_known_args()[0]
load_dotenv(options.config)  # will use a sensitive default if -c is omitted

HOST = os.getenv('RTDBIN_HOST', 'localhost')
PORT = int(os.getenv('RTDBIN_PORT', options.port))
MAXSIZE = Byte(os.getenv('RTDBIN_MAXSIZE', '16kiB'))
DEFAULT_LANGUAGE = os.getenv('RTDBIN_DEFAULT_LANGUAGE', 'text')
DEFAULT_MAXUSAGE = int(os.getenv('RTDBIN_DEFAULT_MAXUSAGE', -1))
DEFAULT_LIFETIME = Time(os.getenv('RTDBIN_DEFAULT_LIFETIME', -1))
REDIS_ENABLED = strtobool(os.getenv('REDIS_ENABLED', options.redis_enabled))
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
