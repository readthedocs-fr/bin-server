import bottle

root = __import__("pathlib").Path(__file__).resolve().parent
bottle.TEMPLATE_PATH = [str(root / 'views')]

from . import config
from . import utils
from . import controller
from . import models
