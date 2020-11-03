import bottle as bt
from pathlib import Path
from bin import root, config
from bin.models import Snippet
from bin.utils import parse_language, parse_extension


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
    if int(content_length) > config.MAXSIZE:
        raise bt.HTTPError(413, f"Payload too large, we accept maximum {config.MAXSIZE} bytes")

    files = bt.request.files
    forms = bt.request.forms

    code = None
    ext = parse_extension(config.DEFAULT_LANGUAGE)
    maxusage = config.DEFAULT_MAXUSAGE

    try:
        if files:
            part = next(files.values())
            code = part.file.read(config.MAXSIZE)
            ext = parse_extension(Path(part.filename).suffix.lstrip('.')) or ext
        if forms:
            code = forms.get('code', '').encode('latin-1') or code
            ext = parse_extension(forms.get('lang')) or ext
            maxusage = int(forms.get('maxusage') or maxusage)
        if not code:
            raise ValueError("Code is missing")
    except ValueError as exc:
        raise bt.HTTPError(400, str(exc))

    snippet = Snippet.create(code, max(maxusage, -1))
    bt.redirect(f'/{snippet.id}.{ext}')


@bt.route('/<snippet_id>', method='GET')
@bt.route('/<snippet_id>.<ext>', method='GET')
def get_html(snippet_id, ext=None):
    try:
        snippet = Snippet.get_by_id(snippet_id)
    except KeyError:
        raise bt.HTTPError(404, "Snippet not found")
    language = parse_language(ext)
    return bt.template('highlight', code=snippet.code, language=language)


@bt.route('/raw/<snippet_id>', method='GET')
@bt.route('/raw/<snippet_id>.<ext>', method='GET')
def get_raw(snippet_id, ext=None):
    try:
        snippet = Snippet.get_by_id(snippet_id)
    except KeyError:
        raise bt.HTTPError(404, "Snippet not found")
    return snippet.code
