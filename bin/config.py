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
cli.add_argument('--rtdbin-port', metavar="PORT", type=int, default=8012,
                 help="builtin server port")
cli.add_argument('--rtdbin-config', metavar="PATH",
                 help="dotenv config file")
options = cli.parse_known_args()[0]
load_dotenv(options.rtdbin_config)  # use a sensitive default when omitted

HOST = os.getenv('RTDBIN_HOST', 'localhost')
PORT = int(os.getenv('RTDBIN_PORT', options.rtdbin_port))
MAXSIZE = Byte(os.getenv('RTDBIN_MAXSIZE', '16kiB'))
DEFAULT_LANGUAGE = os.getenv('RTDBIN_DEFAULT_LANGUAGE', 'text')
DEFAULT_MAXUSAGE = int(os.getenv('RTDBIN_DEFAULT_MAXUSAGE', -1))
DEFAULT_LIFETIME = Time(os.getenv('RTDBIN_DEFAULT_LIFETIME', -1))
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
