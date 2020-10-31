import bottle as bt
from bin import root, config
from bin.models import Snippet

languages = [
    ('py', 'python'),
    ('js', 'javascript'),
    ('md', 'markdown'),
    ('cs', 'csharp'),
    ('sh', 'shell'),
    ('kts', 'kotlin'),
    ('h', 'objectivec'),
    ('hpp', 'cpp'),
    ('rb', 'ruby'),
    ('rs', 'rust'),
    ('ts', 'typescript'),
    ('yml', 'yaml'),
    ('txt', 'plaintext'),
]
exttolang = {ext: language for ext, language in languages}
langtoext = {language: ext for ext, language in languages}


@bt.route('/', method='GET')
def get_new_form():
    return bt.template('newform.html')


@bt.route('/assets/<filepath:path>')
def assets(filepath):
    return bt.static_file(filepath, root=root.joinpath('assets'))


@bt.route('/new', method='POST')
def post_new():
    content_length = bt.request.get_header('Content-Length')
    if content_length is None:
        raise bt.HTTPError(411, "Content-Length required")
    if int(content_length) > config.SNIPPET_MAX_SIZE:
        raise bt.HTTPError(413, f"Payload too large, we accept maximum {config.SNIPPET_MAX_SIZE} bytes")

    code = None
    if bt.request.files:
        code = next(bt.request.files.values()).file.read(config.SNIPPET_MAX_SIZE)
    elif bt.request.forms:
        code = bt.request.forms.get('code', '').encode('latin-1')
    if not code:
        raise bt.HTTPError(417, "Missing code")

    ext = ""
    if bt.request.forms:
        lang = bt.request.forms.get('lang')
        if lang:
            ext = "."+langtoext.get(lang, lang)

    snippet = Snippet.create(code.decode('utf-8'))
    bt.redirect(f'/{snippet.id}{ext}')


@bt.route('/<snippet_id>', method='GET')
@bt.route('/<snippet_id>.<ext>', method='GET')
def get_html(snippet_id, ext=None):
    try:
        snippet = Snippet.get_by_id(snippet_id)
    except KeyError:
        raise bt.HTTPError(404, "Snippet not found")
    language = exttolang.get(ext, ext) or 'plaintext'
    return bt.template('highlight', code=snippet.code, language=language)


@bt.route('/raw/<snippet_id>', method='GET')
@bt.route('/raw/<snippet_id>.<ext>', method='GET')
def get_raw(snippet_id, ext=None):
    try:
        snippet = Snippet.get_by_id(snippet_id)
    except KeyError:
        raise bt.HTTPError(404, "Snippet not found")
    return snippet.code
