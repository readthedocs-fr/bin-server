import bottle

root = __import__("pathlib").Path(__file__).resolve().parent
bottle.TEMPLATE_PATH = [str(root / 'views')]
app = application = bottle.default_app()

from . import config
from . import controller
from . import models
