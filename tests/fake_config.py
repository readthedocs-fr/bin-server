from collections import ChainMap, UserDict
from metrics import Byte, Time
from bin import config

real_config = config.asdict()
default_config = {
    'MAXSIZE': Byte('16kiB'),
    'DEFAULT_LANGUAGE': 'text',
    'DEFAULT_MAXSIZE': 0,
    'DEFAULT_LIFETIME': Time(0),
}

class FakeConfig(UserDict):
    def __init__(self):
        self.data = ChainMap({}, default_config, real_config)

    def __getattr__(self, attr):
        return self[attr]