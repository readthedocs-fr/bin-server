import bottle as bt
from bin import root
from bin.models import Snippet

langmap = {
    'py': 'python',
    'js': 'javascript',
    'md': 'markdown',
    'cs': 'csharp',
    'sh': 'shell',
    'kts': 'kotlin',
    'h': 'objectivec',
    'hpp': 'cpp',
    'rb': 'ruby',
    'rs': 'rust',
    'ts': 'typescript',
    'yml': 'yaml',
    'txt': 'plaintext',
}


@bt.route('/', method='GET')
def get_new_form():
    return bt.template('newform.html')


@bt.route('/assets/<filepath:path>')
def assets(filepath):
    return bt.static_file(filepath, root=root.joinpath('assets'))


@bt.route('/new', method='POST')
def post_new():
    code = bt.request.forms.get('code').encode('latin-1').decode('utf-8')
    if not code:
        raise bt.HTTPError(417, "Missing code")
    snippet = Snippet.create(code)
    bt.redirect(f'/{snippet.id}')


@bt.route('/<snippet_id>', method='GET')
@bt.route('/<snippet_id>.<ext>', method='GET')
def get_html(snippet_id, ext=None):
    try:
        snippet = Snippet.get_by_id(snippet_id)
    except KeyError:
        raise bt.HTTPError(404, "Snippet not found")
    language = langmap.get(ext, ext) or 'plaintext'
    return bt.template('highlight', code=snippet.code, language=language)


@bt.route('/raw/<snippet_id>', method='GET')
@bt.route('/raw/<snippet_id>.<ext>', method='GET')
def get_raw(snippet_id, ext=None):
    try:
        snippet = Snippet.get_by_id(snippet_id)
    except KeyError:
        raise bt.HTTPError(404, "Snippet not found")
    return snippet.code
