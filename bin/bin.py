from bottle import route, template, error, static_file
from os import path
from bin import root

@route('/assets/<dir>/<filepath:path>')
def styles(dir=None, filepath=None):
    return static_file(path.join(dir, filepath), root=root.joinpath('assets'))

@route('/', method='GET')
def index():
    return template('index.html')

@route('/new', method='POST')
def publish_new_snippet():
    return 'publish_new_snippet'

@route('/<snippet>', method='GET')
@route('/<snippet>.<ext>', method='GET')
def display_with_coloration(snippet, ext=None):
    return 'display_with_coloration'

@route('/raw/<snippet>', method='GET')
@route('/raw/<snippet>.<ext>', method='GET')
def display_text(snippet, ext=None):
    return 'display_text'

@error(404)
def error404(error):
    return "404"
