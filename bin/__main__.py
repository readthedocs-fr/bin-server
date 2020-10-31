from bottle import run
from bin import config

run(host=config.HOST, port=config.PORT, debug=True)
