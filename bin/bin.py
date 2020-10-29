import bottle
from os import path
from bin import root


@bottle.route(path='/public/<dir>/<filepath:path>')
def static_files(dir=None, filepath=None):
    return bottle.static_file(path.join(dir, filepath), root=root.joinpath('public'))


@bottle.route(path='/', method='GET')
def index():
    return bottle.template('index.html')


@bottle.route(path='/new', method='POST')
def post_new_snippet():
    return 'New snippet'


@bottle.route(path='/<id>', method='GET')
@bottle.route(path='/<id>.<ext>', method='GET')
def get_highlight_snippet(id, ext='txt'):
    return 'Highlight snippet'


@bottle.route(path='/raw/<id>', method='GET')
@bottle.route(path='/raw/<id>.<ext>', method='GET')
def get_raw_snippet(id, ext='txt'):
    return 'Raw snippet'


@bottle.error(code=404)
def error_handler_404(error):
    return f'Error 404: (Page not found) {error}'


@bottle.error(code=500)
def error_handler_500(error):
    return f'Error 500: (Internal server error) {error}'