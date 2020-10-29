import bottle
from os import path
from bin import root


languages_exts = {
    'py': 'python',
    'js': 'javascript',
    'md': 'markdown',
    'cs': 'csharp',
    'sh': 'kotlin',
    'h': 'objectivec',
    'hpp': 'cpp',
    'rb': 'ruby',
    'rs': 'rust',
    'ts': 'typescript',
    'yml': 'yaml',
    'txt': 'plaintext',
    'html': 'html',
    'css': 'css',
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
    return 'New snippet'


@bottle.route(path='/<id>', method='GET')
@bottle.route(path='/<id>.<ext>', method='GET')
def get_highlight_snippet(id, ext='py'):
    code = '@route(\'/raw/<snippet_id>\')\n@route(\'/raw/<snippet_id>.<ext>\', method=\'GET\')\ndef get_raw_snippet(snippet_id, ext=None):\n    return database.get(snippet_id)'
    if code:
        return bottle.template('highlight.html', code=code, lang=languages_exts.get(ext))
    raise bottle.HTTPError(404, 'Snippet not found')


@bottle.route(path='/raw/<id>', method='GET')
@bottle.route(path='/raw/<id>.<ext>', method='GET')
def get_raw_snippet(id, ext='txt'):
    return 'Raw snippet'


@bottle.error()
def error_handler(error):
    return error