import bottle
from genpw import pronounceable_passwd
from os import path
from bin import root

snippets = {}

languages_exts = {
    'py': 'python',
    'js': 'javascript',
    'md': 'markdown',
    'cs': 'csharp',
    'sh': 'kotlin',
    'sh': 'bash',
    'kt': 'kotlin',
    'h': 'objectivec',
    'hpp': 'cpp',
    'cpp': 'cpp',
    'c': 'c',
    'rb': 'ruby',
    'rs': 'rust',
    'ts': 'typescript',
    None: '',
}


@bottle.route(path='/public/<dir>/<filepath:path>')
def static_files(dir=None, filepath=None):
    return bottle.static_file(path.join(dir, filepath), root=root.joinpath('public'))


@bottle.route(path='/', method='GET')
def index():
    return bottle.template('index.html')


@bottle.route(path='/new', method='POST')
def post_new_snippet():
    code = bottle.request.forms.get('code')
    ext = bottle.request.forms.get('lang')
    snippet = pronounceable_passwd(17)
    snippets[snippet] = code
    return bottle.redirect(f'/{snippet}.{ext}')


@bottle.route(path='/<id>', method='GET')
@bottle.route(path='/<id>.<ext>', method='GET')
def get_highlight_snippet(id, ext='txt'):
    code = snippets[id]
    if code:
        return bottle.template('highlight.html', code=code, lang=languages_exts.get(ext))
    raise bottle.HTTPError(404, 'Snippet not found')


@bottle.route(path='/raw/<id>', method='GET')
@bottle.route(path='/raw/<id>.<ext>', method='GET')
def get_raw_snippet(id, ext='txt'):
    return bottle.template('raw.html', code=snippets[id])


@bottle.error()
def error_handler(error):
    return error
