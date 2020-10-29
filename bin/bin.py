from bottle import route, template, error, static_file, request, redirect
from os import path
from bin import root, languageOfExtension
from bin.models.code import get_code_by_snippetId, create_new_snippet

@route('/assets/<dir>/<filepath:path>')
def getAssets(dir=None, filepath=None):
    return static_file(path.join(dir, filepath), root=root.joinpath('assets'))

@route('/', method='GET')
def index():
    return template('index.html')

@route('/new', method='POST')
def publish_new_snippet():
    snippetId = create_new_snippet(request.forms.get("code"))
    redirect(f'/{snippetId}')

@route('/<snippetId>', method='GET')
@route('/<snippetId>.<ext>', method='GET')
def display_with_coloration(snippetId, ext=None):
    code = get_code_by_snippetId(snippetId)
    language = languageOfExtension[ext] if ext in languageOfExtension else ""
    return template('coloration', code=code, language=language)

@route('/raw/<snippetId>', method='GET')
@route('/raw/<snippetId>.<ext>', method='GET')
def display_text(snippetId, ext=None):
    return 'display_text'

@error(404)
def error404(error):
    return "404"
