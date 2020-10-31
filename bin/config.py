import os
from argparse import ArgumentParser
from dotenv import load_dotenv

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
options = cli.parse_args()
load_dotenv(options.config)  # will use a sensitive default if -c is omitted

HOST = os.getenv('RTDBIN_HOST', 'localhost')
PORT = int(os.getenv('RTDBIN_PORT', options.port))
SNIPPET_MAX_SIZE = int(os.getenv('RTDBIN_SNIPPET_MAX_SIZE', 16384))
REDIS_ENABLED = strtobool(os.getenv('REDIS_ENABLED', options.redis_enabled))
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
